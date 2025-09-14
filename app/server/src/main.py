from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from datetime import datetime
import os
from typing import List, Optional

# データベース設定
DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://postgres:postgres@sample_db:5432/postgres")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# データベースモデル


class TaskModel(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

# Pydanticモデル


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None


class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


# FastAPIアプリケーション初期化
app = FastAPI(
    title="Template Utils API",
    description="React + Python + PostgreSQL サンプルアプリケーションのAPI",
    version="1.0.0"
)

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://client:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# データベース依存性


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# データベーステーブル作成


@app.on_event("startup")
async def startup_event():
    Base.metadata.create_all(bind=engine)

# ルートエンドポイント


@app.get("/")
async def root():
    return {
        "message": "Template Utils API",
        "version": "1.0.0",
        "description": "React + Python + PostgreSQL サンプルアプリケーション"
    }

# ヘルスチェック


@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow()}

# タスク一覧取得


@app.get("/api/tasks", response_model=List[TaskResponse])
async def get_tasks(db: Session = Depends(get_db)):
    try:
        tasks = db.query(TaskModel).order_by(TaskModel.created_at.desc()).all()
        return tasks
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"データベースエラー: {str(e)}")

# タスク作成


@app.post("/api/tasks", response_model=TaskResponse)
async def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    try:
        db_task = TaskModel(
            title=task.title,
            description=task.description
        )
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return db_task
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"タスクの作成に失敗しました: {str(e)}")

# タスク取得（ID指定）


@app.get("/api/tasks/{task_id}", response_model=TaskResponse)
async def get_task(task_id: int, db: Session = Depends(get_db)):
    try:
        task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
        if task is None:
            raise HTTPException(status_code=404, detail="タスクが見つかりません")
        return task
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"データベースエラー: {str(e)}")

# タスク削除


@app.delete("/api/tasks/{task_id}")
async def delete_task(task_id: int, db: Session = Depends(get_db)):
    try:
        task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
        if task is None:
            raise HTTPException(status_code=404, detail="タスクが見つかりません")

        db.delete(task)
        db.commit()
        return {"message": f"タスク ID {task_id} を削除しました"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"タスクの削除に失敗しました: {str(e)}")

# タスク更新


@app.put("/api/tasks/{task_id}", response_model=TaskResponse)
async def update_task(task_id: int, task: TaskCreate, db: Session = Depends(get_db)):
    try:
        db_task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
        if db_task is None:
            raise HTTPException(status_code=404, detail="タスクが見つかりません")

        db_task.title = task.title
        db_task.description = task.description
        db.commit()
        db.refresh(db_task)
        return db_task
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"タスクの更新に失敗しました: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
