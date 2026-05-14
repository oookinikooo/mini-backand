from .routers import accounts, approvals, auth, users

all_routers = [
    accounts.router,
    users.router,
    auth.router,
]
