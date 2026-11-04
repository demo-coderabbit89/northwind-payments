from fastapi import FastAPI

from app.routers import orders, transactions, webhooks

app = FastAPI(title="Northwind Payments", version="1.4.0")
app.include_router(orders.router)
app.include_router(transactions.router)
app.include_router(webhooks.router)
