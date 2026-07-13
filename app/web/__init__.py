from .routers import auth, order, requester, service_type, users

all_routers = [
    auth.router,
    users.router,
    order.router,
    requester.router,
    service_type.router,
]
