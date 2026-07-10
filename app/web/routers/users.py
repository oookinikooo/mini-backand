import logging

from fastapi import APIRouter, HTTPException, status
from src.services.active_directory import Profile
from src.services.user import User, Users

from ..dependencies import DBSessionDep, UserDep

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=User)
async def get_user_info_by_token(user_session: UserDep, db_session: DBSessionDep):
    user_id = user_session["user_id"]

    user_service = Users(db_session)
    user = await user_service.get(user_id)
    if not user:
        raise HTTPException(status_code=401, detail="Not authorize")
    return user


@router.get("/{user_id}", response_model=User)
async def get_user(user_session: UserDep, user_id: int, db_session: DBSessionDep):
    user_service = Users(db_session)
    user = await user_service.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# @router.post("/register", response_model=User)
# async def register_user(user_session: UserDep, db_session: DBSessionDep):
#     user_id = user_session["user_id"]

#     user_service = Users(db_session)
#     user = await user_service.get(user_id)
#     if not user:
#         try:
#             # profile = await ADService().search_by_id(user_id)
#             profile = Profile(
#                 id=user_id,
#                 login="nikolay.adamov",
#                 firstname="Николай",
#                 middle_name="Андреевич",
#                 surname="Адамов",
#                 is_active=True,
#             )
#         except Exception as e:
#             logger.error(f"Get profile from AD failed\n{type(e).__name__}: {e}")

#             raise HTTPException(
#                 status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
#                 detail="Active Directory not response",
#             )

#         if not profile:
#             raise HTTPException(
#                 status_code=status.HTTP_404_NOT_FOUND,
#                 detail=f"Active Directory profile not found by ID {user_id}",
#             )

#         if not profile.is_active:
#             raise HTTPException(
#                 status_code=status.HTTP_403_FORBIDDEN,
#                 detail=f"Active Directory profile exists but disabled for ID {user_id}",
#             )

#         user = await user_service.register(
#             UserAdd(
#                 id=profile.id,
#                 login=profile.login,
#                 firstname=profile.firstname,
#                 middle_name=profile.middle_name,
#                 surname=profile.surname,
#             )
#         )
#         if not user:
#             raise HTTPException(status_code=401, detail="Failed when add user")
#     return user


# @router.get("/data")
# async def get_user_data_v2(db_session: DBSessionDep):
#     user_service = Users(db_session)
#     user = await user_service.get(1)
#     return {"data": f"Hello {user}"}


# @router.get("/test-data")
# async def get_user_data(user_session: UserDep):
#     return {"data": f"Hello {user_session}"}

