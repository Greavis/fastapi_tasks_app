from pydantic import BaseModel, Field
from typing import Literal


class TaskCreate(BaseModel):
    title: str
    description: str = None
    status: Literal["open", "in_progress", "done"] = "open"
    priority: Literal["low", "medium", "high"] = "high"

class TaskUpdate(BaseModel):
    task_id: int = Field(gt=0)
    title: str | None = None
    description: str | None = None
    status: str | None = None
    priority: str | None = None

class TaskResponse(BaseModel):
    id: int = Field(gt=0)
    title: str
    description: str | None = None
    status: Literal["open", "in_progress", "done"]
    priority: Literal["low", "medium", "high"]