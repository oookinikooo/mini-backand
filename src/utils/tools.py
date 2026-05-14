import hashlib
import hmac
import urllib.parse
from operator import itemgetter

from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPBearer

from src.core.config import config

oauth2_schema = HTTPBearer()
router = APIRouter(prefix="/auth", tags=["Users"])


def verify_telegram_init_data(init_data: str) -> dict:
    parsed = dict(urllib.parse.parse_qsl(init_data))
    if "hash" not in parsed:
        raise HTTPException(status_code=400, detail="Missing hash")

    received_hash = parsed.pop("hash")

    data_check_string = "\n".join(
        f"{k}={v}" for k, v in sorted(parsed.items(), key=itemgetter(0))
    )

    secret_key = hmac.new(
        b"WebAppData",
        config.BOT_TOKEN.encode(),
        hashlib.sha256,
    ).digest()

    expected_hash = hmac.new(
        secret_key,
        data_check_string.encode(),
        hashlib.sha256,
    ).hexdigest()

    if not hmac.compare_digest(expected_hash, received_hash):
        raise HTTPException(status_code=403, detail="Invalid auth data")

    return parsed
