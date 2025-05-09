from .service import Task, TaskStatusEnum
from datetime import date
from ..exception import UnChangeableTask


def update_task_status(task: Task):
    # if task.status == TaskStatusEnum.success and task.due_date >= date.today():
    #     task.status = TaskStatusEnum.pending
    #     return task
    # elif task.status == TaskStatusEnum.failed or task.status == TaskStatusEnum.success:
    #     print(f"-----------------XYZZ Printing----------------")
    #     raise UnChangeableTask()
    # elif task.status == TaskStatusEnum.pending and task.due_date < date.today():
    #     if task.is_completed == True:
    #         task.status = TaskStatusEnum.success
    #     else:
    #         task.status = TaskStatusEnum.failed
    #     return task
    # else:
    #     return None
    pass
    
    