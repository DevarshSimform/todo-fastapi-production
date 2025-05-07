import uvicorn
from fastapi import FastAPI


app = FastAPI()


def main():
    uvicorn.run(app, port=8000)


if __name__ == "__main__":
    main()
