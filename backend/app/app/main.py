from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.auth import main as auths
from app.users import main as users
from app.blogs import main as blogs, sub as blogs_sub

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auths.app)
app.include_router(users.app)
app.include_router(blogs.app)
app.include_router(blogs_sub.app)
