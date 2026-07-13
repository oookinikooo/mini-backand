import logging

from fastapi import APIRouter
from src.services.requester import Requester, Requesters

from ..dependencies import DBSessionDep, UserDep

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/requesters", tags=["Order"])


@router.get("/", response_model=list[Requester])
async def get_creators(user_session: UserDep):
    return await Requesters().get_all()
