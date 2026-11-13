from fastapi import APIRouter, HTTPException, status
from schemas.auth_schemas import UserSignIn
from db import user_db

auth_route = APIRouter(tags=["Auth"])

@auth_route.post("/signin")
async def auth_signin(auth : UserSignIn):
    result = await user_db.get_user(auth.email)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="존재하지 않는 이메일입니다.")
    else:
        if result.password != auth.password:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="비밀번호가 틀렸습니다.")
        return {"msg" : "인증성공"}