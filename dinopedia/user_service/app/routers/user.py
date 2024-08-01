from fastapi import APIRouter, HTTPException,Query
from typing import Optional

router = APIRouter()

# Define roles
class Role(str):
    DEV = "dev"
    ADMIN = "admin"

# Mock token data
mock_tokens = {
    "123": Role.DEV,
    "456": Role.ADMIN
}

router = APIRouter()

# Mock function to validate token and get role
def get_role_from_token(token: str) -> str:
    role = mock_tokens.get(token)
    if not role:
        raise HTTPException(status_code=401, detail="Invalid token")
    return role

@router.get("/users/token")
def validate_token(token: Optional[str] = Query(None)):
    if not token:
        raise HTTPException(status_code=400, detail="Token is required")
    role = get_role_from_token(token)
    return {"role": role}
