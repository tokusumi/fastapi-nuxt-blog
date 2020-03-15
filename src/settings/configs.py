import os
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from users.models import User

SECRET_KEY = os.getenv("SECRET_KEY", "test")
JWT_ALGORITHM = "HS256"
JWT_EXPIRRE_KEY = "exp"
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = 30
PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")
OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl="/auth/token")

# require hashed_password columns
USER_MODEL = User
