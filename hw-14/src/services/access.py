from fastapi import Depends, HTTPException
from starlette import status
from starlette.requests import Request

from src.entity.user import Role, User
from src.services.auth import auth_service


class Access:
    def __init__(self, allowed_roles: list[Role]):
        self.allowed_roles = allowed_roles

    def __call__(
        self,
        request: Request,
        current_user: User = Depends(auth_service.get_current_user),
    ):
        if current_user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not allowed to access this resource",
            )
