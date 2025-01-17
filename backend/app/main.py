from fastapi import FastAPI
from routes import users, auth, budgetCategory, wallet, expenses, transactions
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:5173", 
    "http://127.0.0.1:5173", 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)

@app.get('/')
def welcome():
    return {"message": 'welcome to digital wallet'}

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(budgetCategory.router)
app.include_router(wallet.router)
app.include_router(expenses.router)
app.include_router(transactions.router)


