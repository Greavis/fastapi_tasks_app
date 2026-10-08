from fastapi import FastAPI
from typing import Literal

from .tasks import Tasks


app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/tasks")
def read_tasks(status: Literal["open", "in_progress", "done"] | None = None, priority: Literal["low", "medium", "high"] | None = None):
    return Tasks().get_tasks(status, priority)

@app.get("/tasks/{task_id}")
def read_task(task_id: int):
    return Tasks().get_task(int(task_id))

@app.post("/tasks")
def create_task(title: str, description:str =None, status: Literal["open", "in_progress", "done"] = "open", priority: Literal["low", "medium", "high"] ="high"):
    return Tasks().create_task(title, description, status, priority)

@app.patch("/tasks/{task_id}")
def update_task(task_id: int, title:str =None, description:str =None, status: Literal["open", "in_progress", "done"] =None, priority: Literal["low", "medium", "high"] =None):
    return Tasks().update_task(int(task_id), title, description, status, priority)

@app.delete("/tasks/{task_id}")
def delete_task(task_id:int):
    return Tasks().delete_task(int(task_id))