from typing import Annotated

from fastapi import Depends
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPBearer
from jose import jwt
from jose.exceptions import ExpiredSignatureError, JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import config
from src.core.db import get_session

oauth2_schema = HTTPBearer()


async def get_current_user(bearer=Depends(oauth2_schema)):
    try:
        payload = jwt.decode(
            bearer.credentials,
            config.JWT_SECRET_KEY,
            algorithms=config.JWT_ALGORITHM,
        )
        return payload
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


DBSessionDep = Annotated[AsyncSession, Depends(get_session)]
UserDep = Annotated[dict, Depends(get_current_user)]
