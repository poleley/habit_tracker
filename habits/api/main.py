from fastapi import FastAPI
from habits.api import endpoints


app = FastAPI()
app.include_router(endpoints.root)
