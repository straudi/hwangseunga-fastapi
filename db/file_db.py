from fastapi import UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from models import file_model
from schemas.files_schemas import File as FileSchema
from pathlib import Path
import shutil

UPLOAD_DIR = Path("static/files")

async def upload(file:UploadFile, db :Session) -> file_model.File | None:
    filename = Path(file.filename).stem

    exist_file = (db.query(file_model.File)
                  .filter(file_model.File.filename == filename)
                  .first())
    if exist_file:
        return None

    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    file_path = UPLOAD_DIR / file.filename

    try:
        with file_path.open("xb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        fileTable = file_model.File(
                #filename = file.filename, #확장자 포함
                filename = filename,
                file_type = file.content_type or "application/octet-stream",
                file_path= file_path.as_posix()
                #file_path=f"/static/files/{file.filename}"
        )
        db.add(fileTable)
        db.commit()
        db.refresh(fileTable)
        return fileTable

    except Exception:
        db.rollback()
        file_path.unlink(missing_ok=True)
        raise
    
async def download(filename:str, db:Session):
    exist_file = (db.query(file_model.File)
                .filter(file_model.File.filename == filename)  
                .first()
                )
    if exist_file is None :
        return None

    file_path = Path(exist_file.file_path)

    return FileResponse(
        path=file_path,
        filename=file_path.name,
        media_type="application/octet-stream"
    )

async def get_files(db:Session) ->list[FileSchema]:
    fileTable = db.query(file_model.File).all()
    if len(fileTable) == 0:
        return None
    files = [FileSchema.model_validate(file) for file in fileTable]
    return files;


