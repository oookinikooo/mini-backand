import logging

from fastapi import APIRouter
from src.services.service_type import ServiceType, ServiceTypes

from ..dependencies import DBSessionDep, UserDep

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/service-types", tags=["Service Type"])


@router.get("/", response_model=list[ServiceType])
async def get_creators(user_session: UserDep):
    return await ServiceTypes().get_all()
