from fastapi import (
    APIRouter, Depends, HTTPException, Response, status, Request, Body, Path,
    Cookie
)

from app.db.database import get_rep, Repository
from app.api.schemas.all import AuthorDB, UserWithBooksDB, UserWithBooksBookDB, BookWithUsersDB, BookDB, UserDBPublic, GenreDB

from typing import List
from app.api.utils.security import get_password_hash, create_token, require_user, verify_password
from app.api.roles import Role, role_req
from app.log.logger import logger


admin_router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

@admin_router.get('/get_user_info/', response_model=UserDBPublic)
@role_req((Role.ADMIN, Role.S_ADMIN, ))
async def get_user_info(get_id: int,
                        user_id = Depends(require_user), rep: Repository = Depends(get_rep)):
    res = await rep.user.get_one(get_id)
    if res is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Error')
    return res.to_schema_public()


# книги пользователя читаемые/прочитанные
@admin_router.get('/get_user_s__books/', response_model=List[BookDB])
@role_req((Role.ADMIN, Role.S_ADMIN, ))
async def get_user_s__books(get_id: int, returned: bool,
                         item_start: int = 0, item_end: int = 10,
                         user_id = Depends(require_user), rep: Repository = Depends(get_rep)):
    res = await rep.user.get_books(get_id, returned, item_start, item_end)
    if len(res) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Error')
    return [r.to_schema() for r in res]


# жанры книг пользователя читаемые/прочитанные
@admin_router.get('/get_user_s__genres/', response_model=List[GenreDB])
@role_req((Role.ADMIN, Role.S_ADMIN, ))
async def get_user_s__genres(get_id: int, returned: bool,
                          item_start: int = 0, item_end: int = 10,
                          user_id = Depends(require_user), rep: Repository = Depends(get_rep)):
    res = await rep.user.get_genres(get_id, returned, item_start, item_end)
    if len(res) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Error')
    return [r.to_schema() for r in res]


# авторы книг пользователя читаемые/прочитанные
@admin_router.get('/get_user_s__authors/', response_model=List[AuthorDB])
@role_req((Role.ADMIN, Role.S_ADMIN, ))
async def get_user_s__authors(get_id: int, returned: bool,
                           item_start: int = 0, item_end: int = 10,
                           user_id = Depends(require_user), rep: Repository = Depends(get_rep)):
    res = await rep.user.get_authors(get_id, returned, item_start, item_end)
    if len(res) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Error')
    return [r.to_schema() for r in res]


# читатели задержавшие книги сданные/не сданные книги
@admin_router.get('/get_users_overdue/', response_model=List[UserWithBooksBookDB])
@role_req((Role.ADMIN, Role.S_ADMIN, ))
async def get_users_overdue(returned: bool,
                      item_start: int = 0, item_end: int = 10,
                      user_id = Depends(require_user), rep: Repository = Depends(get_rep)):
    res = await rep.user.get_overdue(returned, item_start, item_end)
    if len(res) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Error')
    return [r.to_schema_with_books_book() for r in res]