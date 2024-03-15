from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from todo_app.api.deps import SessionDep, authenticate
from todo_app.core import security
from todo_app.settings import ACCESS_TOKEN_EXPIRE_MINUTES
from todo_app.models import Token

router = APIRouter()


@router.post("/login/access-token")
def login_access_token(
    session: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = authenticate(
        session=session, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    # elif not user.is_active:
    #     raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return Token(
        access_token=security.create_access_token(
            user.id, expires_delta=access_token_expires
        )
    )


# @router.post("/login/test-token", response_model=UserOut)
# def test_token(current_user: CurrentUser) -> Any:
#     """
#     Test access token
#     """
#     return current_user

