"""Demo auth: bearer tokens map to users. Real service uses OIDC."""
from dataclasses import dataclass

from fastapi import Header, HTTPException


@dataclass(frozen=True)
class User:
    id: int
    roles: frozenset[str]

    def is_admin(self) -> bool:
        return "admin" in self.roles


_TOKENS = {
    "token-alice": User(id=1, roles=frozenset({"customer"})),
    "token-bob": User(id=2, roles=frozenset({"customer"})),
    "token-ops": User(id=99, roles=frozenset({"admin"})),
}


def current_user(authorization: str = Header(...)) -> User:
    scheme, _, token = authorization.partition(" ")
    user = _TOKENS.get(token) if scheme.lower() == "bearer" else None
    if user is None:
        raise HTTPException(status_code=401, detail="invalid token")
    return user


def require_owner_or_admin(user: User, customer_id: int) -> None:
    if not (user.is_admin() or user.id == customer_id):
        raise HTTPException(status_code=404, detail="not found")
