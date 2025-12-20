from typing import Annotated
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException, Query, status

from sqlmodel import select
from auth import get_current_active_user
from schema import User, Blog, SessionDep
from model.blog import *

router = APIRouter()

@router.post('/query', response_model=list[BlogPublic])
def query(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,):
    stmt = select(Blog).offset(offset).limit(limit)
    return session.exec(stmt).all()


@router.post("/create", response_model=BlogPublic)
async def create(session: SessionDep, form: BlogCreate, current_user: User = Depends(get_current_active_user)):
    entity = Blog.model_validate(form)
    entity.user_id = current_user.id
    entity.user_name = current_user.username
    session.add(entity)
    session.commit()
    session.refresh(entity)
    return entity

@router.put("/detail/{blog_id}", response_model=Blog)
async def select_one(session: SessionDep, blog_id: str, form: BlogUpdate):
    entity = session.get(Blog, blog_id)
    if entity is None:
        raise HTTPException(status_code=404, detail="Blog not found")
    form_data = form.model_dump(exclude_none=True)
    if not form_data:
        raise HTTPException(status_code=400, detail="Blog unset attr")
    for field, value in form_data.items():
        setattr(entity, field, value)
    entity.updated_at = datetime.now()
    session.add(entity)
    session.commit()
    session.refresh(entity)
    return entity

@router.get("/detail/{blog_id}", response_model=Blog)
async def select_one(session: SessionDep, blog_id: str):
    #stmt = select(Blog).where(Blog.id == blog_id)
    #session.exec(stmt).one()
    entity = session.get(Blog, blog_id)
    if entity is None:
        raise HTTPException(status_code=404, detail="Blog not found")
    return entity

@router.delete("/detail/{blog_id}")
async def delete_one(session: SessionDep, blog_id: str):
    #stmt = delete(Blog).where(Blog.id == blog_id)
    #session.exec(stmt)
    #session.commit()
    entity = session.get(Blog, blog_id)
    if entity is None:
        raise HTTPException(status_code=404, detail="Blog not found")
    session.delete(entity)
    session.commit()
    return "ok"

