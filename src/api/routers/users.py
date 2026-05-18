import logging

from fastapi import APIRouter, HTTPException, status

from src.api.dependencies import DBSessionDep, UserDep
from src.models.enums import Domain
from src.modules.user import User, UserAdd, UserService
from src.modules.user import User as UserSchema
from src.utils.active_directory import ADService, Profile

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/users", tags=["Users"])


# @router.get("/{user_id}", response_model=User)
# async def get_user_info(user_id: int, db_session: DBSessionDep):
#     user_service = UserService(db_session)
#     user = await user_service.get(user_id)
#     if not user:
#         raise HTTPException(status_code=401, detail="Not authorize")
#     return user


@router.get("/", response_model=User)
async def get_user_info_by_token(user_session: UserDep, db_session: DBSessionDep):
    user_id = user_session["user_id"]

    user_service = UserService(db_session)
    user = await user_service.get(user_id)
    if not user:
        raise HTTPException(status_code=401, detail="Not authorize")
    return user


@router.post("/register", response_model=User)
async def register_user(user_id: int, db_session: DBSessionDep):
    user_service = UserService(db_session)
    user = await user_service.get(user_id)
    if not user:
        try:
            # profile = await ADService().search_by_id(user_id)
            profile = Profile(
                id=user_id,
                login="nikolay.adamov",
                firstname="Николай",
                middle_name="Андреевич",
                surname="Адамов",
                is_active=True,
            )
        except Exception as e:
            logger.error(f"Get profile from AD failed\n{type(e).__name__}: {e}")

            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Active Directory not response",
            )

        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Active Directory profile not found by ID {user_id}",
            )

        if not profile.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Active Directory profile exists but disabled for ID {user_id}",
            )

        user = await user_service.register(
            UserAdd(
                id=profile.id,
                login=profile.login,
                firstname=profile.firstname,
                middle_name=profile.middle_name,
                surname=profile.surname,
            )
        )
        if not user:
            raise HTTPException(status_code=401, detail="Failed when add user")
    return user


@router.get("/data")
async def get_user_data_v2(db_session: DBSessionDep):
    user_service = UserService(db_session)
    user = await user_service.get(1)
    return {"data": f"Hello {user}"}


@router.get("/test-data")
async def get_user_data(user_session: UserDep):
    return {"data": f"Hello {user_session}"}


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
