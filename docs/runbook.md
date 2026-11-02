# Payments service runbook

## Run locally
1. `pip install -r requirements.txt`
2. `uvicorn app.main:app --reload`
3. Open http://localhost:8000/docs

## On-call
- Capture failures: check the `audit_log` table for the order id, then the `transactions` table.
- Escalate refund disputes to #payments-oncall.
