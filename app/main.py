from fastapi import Depends, FastAPI, Header, HTTPException

from users import main as users
from blogs import main as blogs, sub as blogs_sub

app = FastAPI()


app.include_router(users.app)
app.include_router(blogs.app)
app.include_router(blogs_sub.app)
