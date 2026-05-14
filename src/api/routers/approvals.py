from fastapi import APIRouter

from src.api.dependencies import DBSessionDep, UserDep
from src.modules.account import AccountAdd, AccountService

router = APIRouter(prefix="/approvals", tags=["Approvals"])


@router.get("")
async def some(user_session: UserDep, db_session: DBSessionDep):
    user_id = user_session["user_id"]
    pass

    # account = AccountService(session)
    # new_account = await account.create(data)
    # print(new_account)
