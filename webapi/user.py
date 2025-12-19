from typing import Annotated
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.security import OAuth2PasswordRequestForm

from sqlmodel import select
from schema import UserBase, User, SessionDep
from model.user import *
from auth import authenticate_user,get_current_active_user, create_access_token,ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter()

@router.post('/query', response_model=list[UserPublic])
def query(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,):
    stmt = select(User).offset(offset).limit(limit)
    return session.exec(stmt).all()

@router.post("/token")
async def login_for_access_token(session: SessionDep, form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserPublic)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user