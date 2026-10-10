from fastapi_users import FastAPIUsers
from fastapi_users.authentication import JWTStrategy, BearerTransport, AuthenticationBackend
from fastapi_users.db import SQLAlchemyUserDatabase
from my_app.models.models import User
from my_app.data.my_base import get_db
import uuid

bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=settings.SECRET_KEY, lifetime_seconds=3600)

auth_backend =  AuthenticationBackend(
    name = "jwt",
    transport = bearer_transport,
    get_strategy = get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_db,
    [auth_backend]
)
