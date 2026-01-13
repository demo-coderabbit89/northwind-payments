from fastapi import FastAPI

from app.routers import orders, transactions

app = FastAPI(title="Northwind Payments", version="1.4.0")
app.include_router(orders.router)
app.include_router(transactions.router)
