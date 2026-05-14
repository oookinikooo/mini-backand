from .routers import accounts, approvals, auth, users

all_routers = [
    auth.router,
    users.router,
    accounts.router,
    approvals.router,
]
