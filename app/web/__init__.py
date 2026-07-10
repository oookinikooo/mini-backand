from .routers import auth, creator, order, users

all_routers = [
    auth.router,
    users.router,
    order.router,
    creator.router,
]
