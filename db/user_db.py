from schemas.user_schemas import User
from sqlalchemy.orm import Session
from models import user_model
from schemas.user_update_schema import UserUpdate

users : list[User] = [
    User(username="aaa", password="aaa", email="aaa@aaa.com", name="서강준"),
    User(username="bbb", password="bbb", email="bbb@bbb.com", name="정재현")
]

# async def get_users() -> list[User]:
#     return users

async def get_users(db:Session) -> list[User]:
    userTable = db.query(user_model.User).all()
    print ("user table : ", userTable)
    if len(userTable) == 0: #not userTable
        return None
    users = [User.model_validate(user) for user in userTable]
    '''
    users = []
    for user in userTable: #userTable = [객체1, 객체2]
        users.append( User.model_validate(user)) #db모델 -> 스키마변환
    '''
    return users

# async def get_user(email : str, db : Session) -> User | None:
#     print("email 데이터 베이스 연결 :", email)
#     for u in users:
#         if u.email == email:
#             return u  
#     return None

async def get_user(email : str, db : Session) -> User | None:
    print("email 데이터 베이스 연결 :", email)

    exist_user= (db.query(user_model.User)
                .filter(user_model.User.email == email)
                .first())
    if not exist_user:
        return None  
    return User.model_validate( exist_user )

async def insert( user : User, db : Session ) -> User | None:
    exist_user = ( db.query(user_model.User)
                  .filter(user_model.User.username == user.username)
                  .first())
    if exist_user:
        return None
    userTable = user_model.User(**user.model_dump() )
    print("저장 전 확인 : ", userTable)
    db.add(userTable) #insert
    db.commit()
    db.refresh(userTable) #저장된 정보를 다시 가져옴
    print("저장 후 확인 : ", userTable)
    return user

# async def insert( user : User ) -> User | None:
#     #print("insert user : ", user)
#     for u in users:
#         if u.username == user.username:
#             return None
#     users.append( user )
#     return user

async def update( username:str, user:UserUpdate, db:Session ):
    user_table = ( db.query(user_model.User)
                    .filter(user_model.User.username == username)
                    .first())
    if user_table is None:
        return None
    #user_table.email = user.email # 속성이 적을 때는 이렇게 직접 명시해도 됨
    #user_table.name = user.name

    user_dict = user.model_dump(exclude_unset=True)
    print("user_dict : ", user_dict)

    for k, v in user_dict.items():
        setattr(user_table, k, v)

    db.commit()
    db.refresh(user_table)
    return User.model_validate( user_table )

# async def update( username:str, user:User ):
#     for i,u in enumerate(users):
#         if u.username == username:
#             users[i] = user
#             return user
#     return None

async def delete( username:str):
    for i,u in enumerate(users):
        if u.username == username:
            del_user = users.pop(i)
            return del_user
    return None

async def db_delete_byId(del_id:int, db:Session) :
    del_user = ( db.query(user_model.User)
                .filter(user_model.User.id == del_id)
                .first())
    if del_user is None : 
        return None
    result = User.model_validate( del_user )
    db.delete(del_user)
    db.commit()
    return result

async def db_delete_byEmail(email:str, db:Session) :
    del_user = (db.query(user_model.User)
               .filter(user_model.User.email == email)
               .first()
            ) 
    if del_user is None :
        return None

    result = User.model_validate( del_user )
    db.delete(del_user)
    db.commit()
    return result

async def db_get_one(id:int, db:Session) -> User | None:
    userTable = db.get(user_model.User, id)
    if not userTable:
        return None
    return User.model_validate( userTable )