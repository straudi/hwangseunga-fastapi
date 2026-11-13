from fastapi import APIRouter, HTTPException, status
from schemas.user_schemas import User
from db import user_db

from fastapi import Depends
from sqlalchemy.orm import Session
from db.connection import get_db
from schemas.user_update_schema import UserUpdate
from fastapi import Form
import time

user_router = APIRouter(tags=["User"])

@user_router.get("/test2")
async def test2(db : Session = Depends( get_db ) ) -> dict:
    db = get_db()
    print("db : ", db)
    time.sleep(3)
    return {"msg":"test"}

@user_router.get("/test")
async def test() -> dict:
    db = get_db()
    print("db : ", db)
    print('db next : ', next(db))
    time.sleep(3)
    return {"msg":"test"}

@user_router.get("/")
async def get_users(db:Session = Depends(get_db)) -> list[User]:
    users = await user_db.get_users(db)
    print("users : ", users)
    if not users:
        raise HTTPException(status_code=404, detail="데이터가 없습니다.")
    return users

# @user_router.get("/")
# async def get_users() -> list[User] :
#     users = await user_db.get_users(db)
#     print("users : ",users)
#     if not users:
#         raise HTTPException(status_code=404, detail="데이터가 없습니다.")
#     return users

# @user_router.get("/{email}", response_model=User, status_code=201)
# async def get_user(email : str) :
#     user = await user_db.get_user(email)
#     print(user)
#     if user:
#         return user
#     #raise HTTPException(status_code=404, detail="존재하는 사용자 없음")
#     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="존재하는 사용자 없음")

@user_router.get("/{email}", response_model=User, status_code=201)
async def get_user(email : str, db:Session=Depends(get_db)) :
    user = await user_db.get_user(email, db)
    print(user)
    if user:
        return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="존재하는 사용자 없음")

# @user_router.post("/", response_model=User)
# async def post_user(user : User) -> User:
#     print("사용자 추가 router : ", user)
#     result = await user_db.insert( user )
#     if not result: #None 거짓
#         #raise HTTPException(status_code=409, detail="중복된 아이디 입니다.")
#         raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="중복된 아이디 입니다.")
#     return result

@user_router.post("/", response_model=User)
async def post_user(user : User, db : Session = Depends(get_db)) -> User:
    result = await user_db.insert( user, db )
    if not result: #None 거짓
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="중복된 아이디 입니다.")
    return result

@user_router.put("/{username}")
async def update_user( username:str, user:UserUpdate, db:Session=Depends(get_db) ):
    result = await user_db.update(username, user, db)
    if result:
        return result
    raise HTTPException(status_code=404, detail="수정 사용자 사용자 id 없음")

# @user_router.put("/{username}")
# async def update_user( username:str, user:User ):
#     # print("라우터 연결")
#     # print( username )
#     # print( user )
#     result = await user_db.update(username, user)
#     if result:
#         return result
#     raise HTTPException(status_code=404, detail="수정 사용자 사용자 id 없음")
#     #return None

@user_router.put("/form/{username}")
async def update_user_form( username:str, user:UserUpdate=Form(...), db:Session=Depends(get_db) ):
    result = await user_db.update(username, user, db)
    if result:
        return result
    raise HTTPException(status_code=404, detail="수정 사용자 사용자 id 없음")

# @user_router.delete("/{username}")
# async def delete_user(username : str) -> User:
#     result = await user_db.delete(username)
#     if result:
#         return result
#     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="존재하는 사용자 없음")

@user_router.delete("/{del_id}")
async def del_user_id(del_id : int, db:Session=Depends(get_db)) -> User:
    result = await user_db.db_delete_byId(del_id, db)
    if result:
        return result
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="존재하는 사용자 없음" )

@user_router.delete("/del/{email}")
async def del_user(email:str, db:Session=Depends(get_db)):
    result = await user_db.db_delete_byEmail(email, db)
    if result:
        return result
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="존재하는 사용자 없음")

@user_router.get("/one/{id}")
async def get_user_one(id:int, db:Session = Depends(get_db)):
    result = await user_db.db_get_one(id, db)
    if result:
        return result
    raise HTTPException(
        status_code=404, detail="존재하지 않는 사용자"
    )