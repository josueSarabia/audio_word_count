# uvicorn app:app --reload
# http://localhost:8000/uploadfile

# delete reltive path "."
from fastapi import FastAPI
from .routes.upload import uploadRouter
from .routes.results import resultsRouter

app = FastAPI()

app.include_router(uploadRouter)
app.include_router(resultsRouter)


