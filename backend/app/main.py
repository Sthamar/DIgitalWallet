from fastapi import FastAPI
from routes import users, auth, budgetCategory, wallet

app = FastAPI()

@app.get('/')
def welcome():
    return {"message": 'welcome to digital wallet'}

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(budgetCategory.router)
app.include_router(wallet.router)

