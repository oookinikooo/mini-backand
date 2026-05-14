import json
import logging
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPBearer
from jose import jwt
from jose.exceptions import JWTError
from pydantic import BaseModel

from src.core.config import config
from src.utils.tools import verify_telegram_init_data

logger = logging.getLogger(__name__)
oauth2_schema = HTTPBearer()
router = APIRouter(tags=["Users"])


class InitDataRequest(BaseModel):
    initData: str


@router.post("/auth")
async def telegram_auth(request: InitDataRequest):
    try:
        valid_data = verify_telegram_init_data(request.initData)
        user = json.loads(valid_data["user"])

        exp = datetime.now(timezone.utc) + timedelta(
            minutes=config.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
        )
        token = jwt.encode(
            {
                "user_id": user["id"],
                "exp": int(exp.timestamp()),
            },
            config.JWT_SECRET_KEY,
            algorithm=config.JWT_ALGORITHM,
        )
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid Telegram initData")
    else:
        return token
