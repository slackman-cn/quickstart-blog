from typing import Annotated
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException, Query, status

from sqlmodel import select, delete
from schema import PageCategory, PageTag, SessionDep
from model.meta import *

router = APIRouter()

@router.get('/categories', response_model=list[PageCategoryPublic])
def list_category(session: SessionDep):
    stmt = select(PageCategory)
    return session.exec(stmt).all()


@router.post('/category', response_model=PageCategory)
def add_category(session: SessionDep, form: PageCategoryCreate):
    entity = PageCategory.model_validate(form)
    session.add(entity)
    session.commit()
    session.refresh(entity)
    return entity

@router.put("/category/{category_id}")
def update_category(session: SessionDep, category_id: str, form: PageCategoryUpdate):
    entity = session.get(PageCategory, category_id)
    if entity is None:
        raise HTTPException(status_code=404, detail="Category not found")
    form_data = form.model_dump(exclude_none=True)
    if not form_data:
        raise HTTPException(status_code=400, detail="Category unset attr")
    for field, value in form_data.items():
        setattr(entity, field, value)
    entity.updated_at = datetime.now()
    session.add(entity)
    session.commit()
    session.refresh(entity)
    return entity

@router.get("/category/{category_id}", response_model=PageCategory)
async def select_one(session: SessionDep, category_id: str):
    entity = session.get(PageCategory, category_id)
    if entity is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return entity

@router.delete("/category/{category_id}")
def delete_category(session: SessionDep, category_id: str):
    entity = session.get(PageCategory, category_id)
    if entity is None:
        raise HTTPException(status_code=404, detail="Category not found")
    if entity.blog_count > 0:
        raise HTTPException(status_code=400, detail="Category contains Blog")
    session.delete(entity)
    session.commit()
    return "ok"


@router.get('/tags', response_model=list[str])
def query_tags(session: SessionDep, q: str):
    if not q:
        stmt = select(PageTag.name).limit(10)
    else:
        stmt = select(PageTag.name).where(PageTag.name.like(f'{q}%')).limit(10)
    return session.exec(stmt).all()
