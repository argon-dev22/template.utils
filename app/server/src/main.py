from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from datetime import datetime
import os

# データベース設定
DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://postgres:postgres@sample_db:5432/postgres")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# データベースモデル


class ClickLogModel(Base):
    __tablename__ = "click_logs"

    id = Column(Integer, primary_key=True, index=True)
    clicked_at = Column(DateTime, default=datetime.utcnow)

# Pydanticモデル


class HelloResponse(BaseModel):
    message: str
    click_count: int


# FastAPIアプリケーション初期化
app = FastAPI(
    title="Template Utils API",
    description="React + Python + PostgreSQL シンプルなHello Templateアプリ",
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
        "message": "Template Utils API - Hello Template App",
        "version": "1.0.0",
        "description": "React + Python + PostgreSQL シンプルなサンプルアプリケーション"
    }

# ヘルスチェック


@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow()}

# Hello Template エンドポイント


@app.post("/api/hello", response_model=HelloResponse)
async def hello_template(db: Session = Depends(get_db)):
    try:
        # クリックログを保存
        click_log = ClickLogModel()
        db.add(click_log)
        db.commit()

        # 総クリック数を取得
        total_clicks = db.query(func.count(ClickLogModel.id)).scalar()

        return HelloResponse(
            message="Hello Template! 🎉",
            click_count=total_clicks
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"データベースエラー: {str(e)}")

# クリック統計取得


@app.get("/api/stats")
async def get_stats(db: Session = Depends(get_db)):
    try:
        total_clicks = db.query(func.count(ClickLogModel.id)).scalar()
        latest_click = db.query(ClickLogModel).order_by(
            ClickLogModel.clicked_at.desc()).first()

        return {
            "total_clicks": total_clicks,
            "latest_click": latest_click.clicked_at if latest_click else None
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"データベースエラー: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
