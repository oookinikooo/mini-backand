from .routers import auth, order, users

all_routers = [
    auth.router,
    users.router,
    order.router,
]
