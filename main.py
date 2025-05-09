import uvicorn
from typing import Annotated
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from src.todos.controller import router as todo_router
from src.auth.controller import router as auth_router
from src.database import Base, engine


app = FastAPI()

app.include_router(todo_router)
app.include_router(auth_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def main():
    Base.metadata.create_all(engine)
    uvicorn.run(app, port=8000)


if __name__ == "__main__":
    main()
