from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Task
from schema.task import TaskCreate, TaskResponse, TaskUpdateRequest
from auth import get_current_user
from models import User

router = APIRouter(prefix="/tasks", tags=["Tasks"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=TaskResponse)
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role not in ["user", "admin"]:
      raise HTTPException(status_code=403, detail="Not allowed")

    new_task = Task(
        title=task.title,
        description=task.description,
        user_id=current_user.id
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


@router.get("/", response_model=list[TaskResponse])
def get_my_tasks(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Task).filter(Task.user_id == current_user.id).all()

@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_update: TaskUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    match current_user.role:
        case "admin":
            pass

        case "manager":
            if task.user.manager_id != current_user.id:
                raise HTTPException(
                    status_code=403,
                    detail="Not your managed user's task"
                )

        case "user":
            if task.user_id != current_user.id:
                raise HTTPException(
                    status_code=403,
                    detail="Not your task"
                )

        case _:
            raise HTTPException(status_code=403, detail="Invalid role")

    task.title = task_update.title
    task.description = task_update.description
    task.completed = task_update.completed

    db.commit()
    db.refresh(task)
    return task




@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    match current_user.role:
        case "admin":
            pass

        case "manager":
            if task.user.manager_id != current_user.id:
                raise HTTPException(
                    status_code=403,
                    detail="Not your managed user's task"
                )

        case "user":
            if task.user_id != current_user.id:
                raise HTTPException(
                    status_code=403,
                    detail="Not your task"
                )

        case _:
            raise HTTPException(status_code=403, detail="Invalid role")

    db.delete(task)
    db.commit()
    return {"message": "Task deleted"}

