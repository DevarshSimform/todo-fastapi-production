from fastapi import HTTPException, status




class TaskException(HTTPException):
    pass

class UserException(HTTPException):
    pass


class CredentialException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Could not validate credentials", 
            headers={"WWW-Authenticate": "Bearer"}
        )


class TaskNotFound(TaskException):
    def __init__(self, task_id=None):
        message = "Task not found" if task_id is None else f"Task with id {task_id} not found"
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=message)


class UnAuthorisedForTaskUpdate(TaskException):
    def __init__(self):
        message = "Unauthorised to change this task"
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=message)


class UnChangeableTask(TaskException):
    def __init__(self):
        message = "Task couldn't be changed"
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=message)


class UserNotFound(UserException):
    def __init__(self):
        message = "Invalid email or password"
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=message)


class UserCreationException(UserException):
    def __init__(self):
        message = "User already exists with this email"
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=message)