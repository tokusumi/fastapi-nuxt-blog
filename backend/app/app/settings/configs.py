import boto3
import os
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from app.users.models import User

SECRET_KEY = os.getenv("SECRET_KEY", "test")
JWT_ALGORITHM = "HS256"
JWT_EXPIRRE_KEY = "exp"
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv('JWt_ACCESS_TOKEN_EXPIRE_MINUTES', 30)
PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")
OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl="/auth/token")

# require hashed_password columns
USER_MODEL = User


AWS_ACCESS_KEY_ID = os.getenv('aws_access_key', '')
AWS_SECRET_ACCESS_KEY = os.getenv('aws_secret_access_key', '')
AWS_BUCKET_NAME = os.getenv('bucket_name', '')
S3_URL = os.getenv('s3_URL', '')

aws_session = boto3.Session(
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)
