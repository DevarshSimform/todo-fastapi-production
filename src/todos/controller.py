from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    Body,
)
from ..dependency.db import get_db
from sqlalchemy.orm import Session

from . import (
    TaskIn,
    TaskResponse, 
    TaskComplete,
    service
)




router = APIRouter(
    prefix="/todos", 
    tags=["Todos"]
)


@router.get("/", response_model=list[TaskResponse])
def get_todos(db: Session = Depends(get_db)):
    return service.get_todos(db)

@router.post("/", response_model=TaskResponse)
def create_todo(task: TaskIn, db: Session = Depends(get_db)):
    return service.create_todo(task, db)

@router.get("/{task_id}")
def get_todo(task_id: int, db: Session = Depends(get_db)):
    return service.get_todo_by_id(task_id, db)

@router.put("/{task_id}", response_model=TaskResponse)
def update_todo(task_id: int, task: Annotated[TaskIn, Body()], db: Session = Depends(get_db)):
    return service.update_todo(task_id, task, db)

@router.patch("/{task_id}", response_model=TaskResponse)
def change_todo_status(task_id: int, task: TaskComplete, db: Session = Depends(get_db)):
    return service.change_todo_status(task_id, task, db)

@router.delete("/{task_id}")
def delete_todo(task_id: int, db: Session = Depends(get_db)):
    return service.delete_todo(task_id, db)