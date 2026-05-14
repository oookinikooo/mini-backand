import logging

from fastapi import APIRouter, HTTPException, status

from src.api.dependencies import DBSessionDep, UserDep
from src.models.enums import Domain
from src.modules.user import User as UserSchema
from src.modules.user import UserAdd, UserService
from src.utils.active_directory import ADService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/data")
async def get_user_data_v2(db_session: DBSessionDep):
    user_service = UserService(db_session)
    user = await user_service.get(1)
    return {"data": f"Hello {user}"}


@router.get("/test-data")
async def get_user_data(user_session: UserDep):
    return {"data": f"Hello {user_session}"}


# @router.post("/sync-from-ad", response_model=UserSchema)
# async def register_using_active_directory(user_id: int, session: DBSessionDep):
#     user_service = UserService(session)
#     user = await user_service.get(user_id)
#     if user:
#         raise HTTPException(
#             status_code=status.HTTP_409_CONFLICT,
#             detail=f"User with ID {user.id} already exist",
#         )

#     try:
#         profile = await ADService().search_by_id(user_id)
#     except Exception as e:
#         logger.error(f"Get profile from AD failed\n{type(e).__name__}: {e}")

#         raise HTTPException(
#             status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
#             detail="Active Directory not response",
#         )

#     if not profile:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Active Directory profile not found by ID {user_id}",
#         )

#     if not profile.is_active:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail=f"Active Directory profile exists but disabled for ID {user_id}",
#         )

#     added_user = await user_service.register(
#         UserAdd(
#             id=profile.id,
#             login=profile.login,
#             firstname=profile.firstname,
#             middle_name=profile.middle_name,
#             surname=profile.surname,
#         )
#     )
#     return added_user


# # @router.post("/")
# # async def register_user(
# #     data: UserAdd,
# #     session: SessionDep,
# # ):
# #     user_service = UserService(session)
# #     user = await user_service.get(data.id)
# #     if user:
# #         raise HTTPException(
# #             status_code=status.HTTP_409_CONFLICT,
# #             detail=f"User with ID {user.id} already exist",
# #         )

# #     added_user = await user_service.register(data)

# #     return "ok"
# #     # await account.get_by_user()
# #     # await AccountService.create(AccountAdd(
# #     #     user_id=1,
# #     #     domain=Domain.SD,
# #     #     token='some'
# #     # ))


# # @router.get("/{user_id}", response_model=UserSchema)
# # async def get_user(user_id: int, session: SessionDep):
# #     user_service = UserService(session)
# #     user = await user_service.get(user_id)
# #     if not user:
# #         raise HTTPException(
# #             status_code=status.HTTP_404_NOT_FOUND,
# #             detail=f"User with ID {user_id} not found",
# #         )
# #     return user
