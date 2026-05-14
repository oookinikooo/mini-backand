from fastapi import APIRouter, Depends

from src.api.dependencies import DBSessionDep
from src.core.db import get_session
from src.models.enums import Domain
from src.modules.account import AccountAdd, AccountService
from src.modules.user import UserService

router = APIRouter(prefix="/accounts", tags=["Accounts"])


@router.post("")
async def register_account(
    data: AccountAdd,
    session: DBSessionDep,
):

    account = AccountService(session)
    new_account = await account.create(data)
    print(new_account)
    # await account.get_by_user()
    # await AccountService.create(AccountAdd(
    #     user_id=1,
    #     domain=Domain.SD,
    #     token='some'
    # ))

    # user_service = UserService(session)
    # user = await user_service.get(data.id)
    # if user:
    #     raise HTTPException(
    #         status_code=status.HTTP_409_CONFLICT,
    #         detail=f"User with ID {user.id} already exist"
    #     )

    # added_user = await user_service.register(data)
