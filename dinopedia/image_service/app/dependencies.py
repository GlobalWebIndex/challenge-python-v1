# dependencies.py
from fastapi import Depends, HTTPException, Query
import httpx

USER_SERVICE_URL = "http://user_service:8003"

async def get_user_role(token: str = Query(...)) -> str:
    """
    Validate the token with the user service and retrieve the user's role.

    Args:
        token (str): The authentication token.

    Returns:
        str: The user's role.

    Raises:
        HTTPException: If the token is invalid or the role is not found.
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{USER_SERVICE_URL}/users/token", params={"token": token})
        if response.status_code != 200:
            raise HTTPException(status_code=401, detail="Invalid token")
        role = response.json().get("role")
        if not role:
            raise HTTPException(status_code=401, detail="Role not found in token")
        return role

async def admin_role(token: str = Depends(get_user_role)) -> str:
    """
    Dependency to check if the user has an admin role.

    Args:
        token (str): The authentication token.

    Returns:
        str: The user's role.

    Raises:
        HTTPException: If the user is not an admin.
    """
    if token != "admin":
        raise HTTPException(status_code=403, detail="Access forbidden: Admin only")
    return token

async def dev_role(token: str = Depends(get_user_role)) -> str:
    """
    Dependency to check if the user has a developer role.

    Args:
        token (str): The authentication token.

    Returns:
        str: The user's role.

    Raises:
        HTTPException: If the user is not a developer.
    """
    if token != "dev":
        raise HTTPException(status_code=403, detail="Access forbidden: Dev only")
    return token

