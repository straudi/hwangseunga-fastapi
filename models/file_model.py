from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, DateTime
from datetime import datetime, timezone
from db.connection import Base

class File(Base):
    __tablename__ = "files"

    id : Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    #username : Mapped[str] = mapped_column(String(100))
    filename : Mapped[str] = mapped_column(String(200), unique=True) # 파일명으로 다운로드 하기때문
    uploaded_at : Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )
    file_type : Mapped[str] = mapped_column(String(100))
    file_path : Mapped[str] = mapped_column(String(500), unique=True)