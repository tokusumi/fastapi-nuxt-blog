from fastapi import Depends, FastAPI, Header, HTTPException

from users import main as users
from blogs import main as blogs

app = FastAPI()


app.include_router(users.app)
app.include_router(blogs.app)
