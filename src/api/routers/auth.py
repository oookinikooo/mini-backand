import json
import logging
import secrets
from datetime import datetime, timedelta

from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPBearer
from jose import JWTError, jwt
from pydantic import BaseModel

from src.core.config import config
from src.utils.tools import verify_telegram_init_data

logger = logging.getLogger(__name__)
oauth2_schema = HTTPBearer()
router = APIRouter(prefix="/auth", tags=["Users"])

active_session = {}


class InitDataRequest(BaseModel):
    initData: str


@router.post("/telegram")
async def telegram_auth(request: InitDataRequest):
    try:
        valid_data = verify_telegram_init_data(request.initData)
        user_data = json.loads(valid_data["user"])
        user_id = user_data["id"]

        session_id = secrets.token_urlsafe(16)
        jwt_token = jwt.encode(
            {
                "user_id": user_id,
                "session_id": session_id,
                "exp": datetime.utcnow() + timedelta(minutes=1),
            },
            config.JWT_SECRET_KEY,
            algorithm=config.JWT_ALG,
        )
        # active_session[session_id] = {
        #     "user_id": user_id,
        #     "created_at": datetime.utcnow(),
        # }

        data = {
            "token": jwt_token,
            "user": user_data,
        }
        print(data)
    except Exception:
        raise HTTPException(status_code=403, detail="Invalid Telegram auth")
    else:
        return data


# async def get_current_user(token: str = Depends(oauth2_schema)):
#     try:
#         payload = jwt.decode(
#             token,
#             config.JWT_SECRET_KEY,
#             algorithms=config.JWT_ALG,
#         )
#         # user_id = payload.get("user_id")
#         expired = payload.get("exp")
#         print(f"payload: {payload}\nexpired str: {expired}")

#         if expired:
#             raise HTTPException(status_code=401, detail="Session expired")

#         return payload
#     except JWTError:
#         raise HTTPException(status_code=403, detail="Invalid Telegram auth")


# @app.get("/api/user/data")
# async def get_user_data(current_user: dict = Depends(get_current_user)):
#     return {"data": f"Hello {current_user['user_id']}"}


# @app.get("/api/user/test")
# async def get_user_test_data():
#     print("yes, get it")
#     return {"data": "Hello"}
