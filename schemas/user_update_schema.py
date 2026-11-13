from pydantic import BaseModel, EmailStr

class UserUpdate(BaseModel):
    email : EmailStr | None = None
    name : str | None = None