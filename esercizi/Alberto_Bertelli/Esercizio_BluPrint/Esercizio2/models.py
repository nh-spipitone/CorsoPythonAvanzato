from pydantic import BaseModel, Field

class TaskModel(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    description: str | None = None