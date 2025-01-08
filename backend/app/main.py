from fastapi import FastAPI
from routes.users import router

app = FastAPI()

@app.get('/')
def welcome():
    return {"message": 'welcome to digital wallet'}

app.include_router(router)