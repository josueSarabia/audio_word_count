# uvicorn app:app --reload
# http://localhost:8000/uploadfile
from fastapi import FastAPI
from .routes.upload import uploadRouter

app = FastAPI()

app.include_router(uploadRouter)


