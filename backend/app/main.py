from fastapi import FastAPI
from routes import users, auth

app = FastAPI()

@app.get('/')
def welcome():
    return {"message": 'welcome to digital wallet'}

app.include_router(users.router)
app.include_router(auth.router)

