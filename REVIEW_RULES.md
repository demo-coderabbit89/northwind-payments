# Northwind AI review guidelines

These guide LinearB AI code review on every pull request.

- Focus on bugs, security and data exposure first. Skip pure formatting and naming nitpicks.
- Every endpoint that reads or changes an order, refund or transaction must call
  `require_owner_or_admin` or check `user.is_admin()`. Flag endpoints that only authenticate.
- Every change that moves money must call `audit.record(...)` in the same DB transaction (SOX control NW-AUD-01).
- Money is integer cents. Flag any `float` used for an amount.
- SQL must be parameterized. Flag f-strings or concatenation in SQL.
- Never log card digits, tokens, secrets or full request bodies.
- Outbound HTTP must set a timeout and only call allow-listed hosts.
- Renaming or removing a response field in `app/models.py` is a breaking change for mobile and partner clients.
