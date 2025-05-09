from ..dependency.db import get_db
from sqlalchemy.orm import Session
from datetime import date
from . import (
    TaskIn,
    TaskResponse, 
    TaskComplete
)
from src.entities import (
    Task, 
    TaskStatusEnum, 
    PriorityEnum, 
    User
)
from ..exception import (
    TaskNotFound, 
    UnAuthorisedForTaskUpdate, 
    UnChangeableTask
)
from .utils import update_task_status



def get_todos(user: User, db: Session):
    tasks = db.query(Task).filter(Task.created_by==user.id)
    if len(list(tasks)) == 0:
        print("-----------INSIDE LOOP-------------")
        raise TaskNotFound()
    return tasks


def create_todo(task: TaskIn, user: User, db: Session):
    new_task = Task(
        title=task.title,
        description=task.description,
        priority=task.priority,
        due_date=task.due_date,
        created_by = user.id
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


def get_todo_by_id(id: int, user: User, db: Session):
    task = db.query(Task).filter(Task.id==id, Task.created_by==user.id).first()
    if not task:
        raise TaskNotFound(id)
    return task


def update_todo(id: int, task: TaskIn, user: User, db: Session):
    db_task = db.query(Task).filter(Task.id==id, Task.created_by==user.id)
    if not db_task.first():
        raise TaskNotFound(id)
    db_task.update(task.model_dump(), synchronize_session=False)
    db.commit()
    return db_task.first()
    

def change_todo_status(id: int, task: TaskComplete, user: User, db: Session): 
    db_task = db.query(Task).get(id)
    if not db_task:
        raise TaskNotFound(id)
    if db_task.created_by != user.id:
        raise UnAuthorisedForTaskUpdate()
    if db_task.status == TaskStatusEnum.success or db_task.status == TaskStatusEnum.failed:
        raise UnChangeableTask()

    db_task.is_completed = task.is_completed
    if db_task.is_completed == True:
        db_task.status = TaskStatusEnum.success
    else:
        db_task.status = TaskStatusEnum.failed

    db.commit()
    db.refresh(db_task)
    return db_task 


def delete_todo(id: int, user: User, db: Session):
    db_task = db.query(Task).filter(Task.id == id, Task.created_by == user.id)
    if not db_task.first():
        raise TaskNotFound(id)
    db_task.delete()
    db.commit()
    return {"detial": "Task deleted successfully"}