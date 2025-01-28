from fastapi import FastAPI, WebSocketDisconnect, Depends, WebSocket, HTTPException, status
from routes import users, auth, budgetCategory, wallet, expenses, transactions
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import get_db
from core.security import role_required
from oauth2 import get_current_user, verify_token_access
from models.users import User
from models.transaction import Transaction
from typing import List
from sqlalchemy.sql import func
from decimal import Decimal


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




class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        print("hello")
        await websocket.accept()
        self.active_connections.append(websocket)
    
    async def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        
    async def broadcast(self, msg: dict):
        for connection in self.active_connections:
            print(f"broadcasting message {msg}")
            await connection.send_json(msg)


manager = ConnectionManager()

async def update_realtime_data(user_id: int, db: Session):
    income = db.query(func.sum(Transaction.amount)).filter(
        Transaction.transaction_type.in_(['credit', 'receive']),
        Transaction.user_id == user_id
    ).scalar() or 0
    expense = db.query(func.sum(Transaction.amount)).filter(
        Transaction.transaction_type.in_(['debit', 'send']),
        Transaction.user_id == user_id
    ).scalar() or 0
    
    income = float(income) if isinstance(income, Decimal) else income
    expense = float(expense) if isinstance(expense, Decimal) else expense
    
    print(f"Calculated Income: {income}, Expense: {expense}")
    await manager.broadcast({"income": income, "expense": expense})
       

@app.websocket("/ws/transactions")
async def websocket_endpoint(websocket: WebSocket, db: Session = Depends(get_db)):
    # Extract the token manually from the query parameters
    query_params = websocket.query_params
    token = query_params.get("token")
    
    if not token:
        await websocket.close()
        return
    
    # Verify the token and get the user
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        token_data = verify_token_access(token, credentials_exception)
        
        user = db.query(User).filter(User.id == int(token_data.username)).first()

        if not user:
            raise credentials_exception
    except HTTPException:
        await websocket.close()
        return
    
    # Connect the WebSocket
    await manager.connect(websocket)
    try:
        while True:
            print("before")
            await websocket.receive_text()
            print("after")
            await update_realtime_data(user.id, db)
    except WebSocketDisconnect:
        await manager.disconnect(websocket)




