from ..dependency.db import get_db
from . import (
    TaskIn,
    TaskResponse, 
    TaskComplete
)
from fastapi import (
    Depends, 
    HTTPException, 
    status
)
from ..entities import Task, TaskStatusEnum, PriorityEnum
from sqlalchemy.orm import Session
from datetime import date




def get_todos(db: Session):
    tasks = db.query(Task).all()
    return tasks


def create_todo(task: TaskIn, db: Session):
    new_task = Task(
        title=task.title,
        description=task.description,
        priority=task.priority,
        due_date=task.due_date
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


def get_todo_by_id(id: int, db: Session):
    task = db.query(Task).filter(Task.id == id).first()
    if not task:
        pass
    return task


def update_todo(id: int, task: TaskIn, db: Session):
    db_task = db.query(Task).filter(Task.id == id)
    if not db_task.first():
        pass
    db_task.update(task.model_dump(), synchronize_session=False)
    db.commit()
    return db_task.first()
    

def change_todo_status(id: int, task: TaskComplete, db: Session):
    db_task = db.query(Task).get(id)
    if not db_task:
        pass
    if db_task.status == TaskStatusEnum.success and db_task.due_date >= date.today() and task.is_completed == False:
        db_task.status = TaskStatusEnum.pending
    elif db_task.status == TaskStatusEnum.failed or db_task.status == TaskStatusEnum.success:   
        raise HTTPException(
            detail=f"Cannot change the status to success because the task is already done",
            status_code = status.HTTP_400_BAD_REQUEST
        )
    db_task.is_completed = task.is_completed
    if task.is_completed == True and db_task.due_date >= date.today():
        db_task.status = TaskStatusEnum.success
    db.commit()
    db.refresh(db_task)
    return db_task 


def delete_todo(id: int, db: Session):
    db_task = db.query(Task).filter(Task.id == id)
    if not db_task.first():
        pass
    db_task.delete()
    db.commit()
    return {"detial": "Task deleted successfully"}