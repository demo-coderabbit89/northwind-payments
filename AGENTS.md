# Northwind Payments: engineering standards

These rules apply to humans and AI coding agents alike.

1. **Money is integer cents.** Never use `float` for amounts. Field names end in `_cents`.
2. **Authorization on every resource.** Any endpoint that reads or changes an order, refund or
   transaction must call `require_owner_or_admin` (or check `user.is_admin()`).
3. **Audit every money movement.** Captures, refunds and voids must call `audit.record(...)`
   inside the same DB transaction (SOX control NW-AUD-01).
4. **Parameterized SQL only.** No f-strings or string concatenation in SQL. Whitelist any
   user-controlled column names.
5. **No sensitive data in logs.** Never log card numbers, tokens, secrets or full request bodies.
6. **Outbound HTTP** must set a timeout and only call allow-listed hosts.
7. **Public API contract is versioned.** Renaming or removing a response field is a breaking change
   and needs a "Breaking change" section in the PR description and a CHANGELOG entry.
8. **New endpoints need tests** covering the happy path and the authorization failure.
