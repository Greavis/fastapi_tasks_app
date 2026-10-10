from fastapi import FastAPI
from typing import Literal

from .schemas import TaskCreate, TaskUpdate, TaskResponse
from .tasks import Tasks


app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/tasks", response_model=list[TaskResponse])
def read_tasks(
    status: Literal["open", "in_progress", "done"] | None = None,
    priority: Literal["low", "medium", "high"] | None = None,
    search: str | None = None,
    order: Literal["asc", "desc"] | None = None,
    sort_by: Literal["id", "title", "priority"] | None = None
    ):
    return Tasks().get_tasks(status, priority, search, order, sort_by)

@app.get("/tasks/{task_id}", response_model=TaskResponse)
def read_task(task_id: int):
    return Tasks().get_task(task_id)

@app.post("/tasks", response_model=TaskResponse)
def create_task(task: TaskCreate):
    return Tasks().create_task(**task.model_dump())

@app.patch("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task: TaskUpdate):
    return Tasks().update_task(**task.model_dump())

@app.delete("/tasks/{task_id}")
def delete_task(task_id:int):
    return Tasks().delete_task(task_id)