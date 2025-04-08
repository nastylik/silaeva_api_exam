from enum import Enum
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List

app = FastAPI()

@app.get("/", include_in_schema=False)
def read_root():
    return {"message": "Go to /docs or /redoc for documentation"}

class Status(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in progress"
    COMPLETED = "completed"

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: str = Field(default="", max_length=500)
    status: Status

class Task(TaskCreate):
    id: int

tasks = []
current_id = 0

@app.get("/tasks", response_model=List[Task])
def get_tasks():
    return tasks  # Возвращает пустой массив, если задач нет

@app.post("/tasks", response_model=Task, status_code=201)
def create_task(task: TaskCreate):
    global current_id
    current_id += 1
    new_task = Task(id=current_id, **task.dict())
    tasks.append(new_task)
    return new_taska

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, updated_task: TaskCreate):
    for index, task in enumerate(tasks):
        if task.id == task_id:
            updated_data = task.dict()
            updated_data.update(updated_task.dict())
            tasks[index] = Task(**updated_data)
            return tasks[index]
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    global tasks
    initial_length = len(tasks)
    tasks = [task for task in tasks if task.id != task_id]
    if len(tasks) == initial_length:
        raise HTTPException(status_code=404, detail="Task not found")
