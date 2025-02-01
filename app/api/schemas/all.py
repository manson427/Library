from pydantic import BaseModel, Field
from pydantic import constr, EmailStr, conint
from typing import Optional, List
from datetime import date


class UserPassword(BaseModel):
    password: constr(min_length=8, max_length=16)


class UserPasswordConfirm(BaseModel):
    password_confirm: str


class UserHashedPassword(BaseModel):
    hashed_password: str


class UserName(BaseModel):
    name: str


class UserData(BaseModel):
    email: EmailStr
    born: date

# входные данные ендпоинта логин
class UserLogin(UserName, UserPassword):
    pass

# входные данные ендпоинта смены пароля
class UserChangePassword(UserPassword, UserPasswordConfirm):
    pass

# передаётся на запись в базу для создания нового пользователя
class UserAdd(UserName, UserData, UserHashedPassword):
    pass

# входные данные ендпоинта регистрации пользователя
class UserRegister(UserName, UserData, UserChangePassword):
    pass

class AuthorCreate(BaseModel):
    name: str
    biography: str
    born: date

class AuthorDB(AuthorCreate):
    id: int

class UserDBPublic(UserName, UserData):
    id: int
    role_id: int
    verified: bool

class UserDB(UserDBPublic, UserHashedPassword):
    refresh_token: str | None
    verify_code: str | None
    reset_code: str | None

class UserBookDB(BaseModel):
    id: int
    left_id: int
    right_id: int
    get_at: date
    must_return_at: date
    returned_at: date | None
    returned: bool

class GenreCreate(BaseModel):
    name: str
    description: str

class GenreDB(GenreCreate):
    id: int | None

class BookCreate(BaseModel):
    name: str
    description:str
    publish_year: int
    amount: int

class BookDB(BookCreate):
    id: int | None

class BookWithUsersDB(BookDB):
    id: int | None
    users: List[UserBookDB]

class UserBookWithBookDB(UserBookDB):
    book: BookDB

class UserWithBooksDB(UserDBPublic):
    books: List[UserBookDB]

class UserWithBooksBookDB(UserDBPublic):
    books: List[UserBookWithBookDB]
