from typing import Annotated

from fastapi import Depends
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import config
from src.core.db import get_session

oauth2_schema = HTTPBearer()


async def get_current_user(token: str = Depends(oauth2_schema)):
    try:
        payload = jwt.decode(
            token,
            config.JWT_SECRET_KEY,
            algorithms=config.JWT_ALG,
        )
        # user_id = payload.get("user_id")
        expired = payload.get("exp")
        print(f"payload: {payload}\nexpired str: {expired}")

        if expired:
            raise HTTPException(status_code=401, detail="Session expired")

        return payload
    except JWTError:
        raise HTTPException(status_code=403, detail="Invalid Telegram auth")


DBSessionDep = Annotated[AsyncSession, Depends(get_session)]
UserDep = Annotated[dict, Depends(get_current_user)]
