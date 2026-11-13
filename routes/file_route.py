from fastapi import APIRouter, HTTPException, status, Depends, UploadFile, File, Form
from db import file_db
from sqlalchemy.orm import Session
from db.connection import get_db
from schemas.files_schemas import File as FileSchema

file_route = APIRouter(tags=["File"])

@file_route.post("/upload")
async def file_upload(file:UploadFile=File(...), db:Session=Depends(get_db)):
    result = await file_db.upload(file, db)
    if not result:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="이미 업로드된 파일명입니다.")
    return result
    
@file_route.get("/download/{filename}")
async def file_download( filename : str, db:Session=Depends(get_db)):
    result = await file_db.download(filename, db)
    if not result:
        raise HTTPException(status_code=404, detail="해당 파일 없음")    
    return result

@file_route.get("/")
async def get_files(db:Session=Depends(get_db))->list[FileSchema]:
    files = await file_db.get_files(db)
    if not files:
        raise HTTPException(status_code=404, detail="데이터가 없습니다.")
    return files