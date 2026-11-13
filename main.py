import uvicorn
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from routes.users_routes import user_router
from routes.auth_route import auth_route
from routes.file_route import file_route

from contextlib import asynccontextmanager

from models import user_model
from db.connection import Base, engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("--- 서버 시작 시 설정 내용 ---")
    #print(Base.metadata.tables)
    Base.metadata.create_all(bind=engine)
    yield
    print("--- 서버 종료 시 설정 내용 ---")

app = FastAPI(lifespan=lifespan)

app.include_router(user_router, prefix="/users")
app.include_router(auth_route, prefix="/auth")
app.include_router(file_route, prefix="/file")

@app.get("/")
async def index(request: Request):
    return {
        "index": "success",
        "client_ip": request.client.host if request.client else None
    }

from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], #["http://localhost:3000", "...."]
    allow_methods=["*"], # http 메소드 허용(get, post 등)
    allow_headers=["*"]  # http 통신 헤더 받을 시(front 전달)
)

# 정적 파일 경로 설정
app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
