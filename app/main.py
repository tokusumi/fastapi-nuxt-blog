from fastapi import Depends, FastAPI, Header, HTTPException

from users import main as users

app = FastAPI()


app.include_router(users.app)
