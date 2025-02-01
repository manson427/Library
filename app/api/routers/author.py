
from fastapi import (
    APIRouter, Depends, HTTPException, Response, status, Request, Body, Path,
    Cookie
)

from app.api.schemas.all import AuthorCreate, AuthorDB, GenreDB, UserDB, BookDB, UserDBPublic

from typing import List
from app.db.database import get_rep, Repository
from app.api.utils.security import get_password_hash, create_token, require_user, verify_password
from app.api.roles import Role, role_req
from app.log.logger import logger


author_router = APIRouter(
    prefix="/author",
    tags=["Author"]
)


@author_router.get('/get_one/', response_model=AuthorDB)
async def get_one(author_id: int,
                  rep: Repository = Depends(get_rep)):
    res = await rep.author.get_one(author_id)
    if res is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Error')
    return res.to_schema()


@author_router.get('/get/', response_model=List[AuthorDB])
async def get(item_start: int = 0, item_end: int = 10,
              rep: Repository = Depends(get_rep)):
    res = await rep.author.get(item_start, item_end)
    if len(res) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Error')
    return [r.to_schema() for r in res]


@author_router.get('/get_like/', response_model=List[AuthorDB])
async def get_like(phrase: str,
                   item_start: int = 0, item_end: int = 10,
                   rep: Repository = Depends(get_rep)):
    res = await rep.author.get_names_like(phrase, item_start, item_end)
    if len(res) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Error')
    return [r.to_schema() for r in res]


@author_router.post('/create/', response_model=AuthorDB)
@role_req((Role.ADMIN, Role.S_ADMIN, ))
async def create(author: AuthorCreate,
                 user_id=Depends(require_user), rep: Repository = Depends(get_rep)):
    res = await rep.author.create(author.model_dump())
    if res is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail='Error')
    author = res.to_schema()
    logger.debug(f"Author with id={author.id} created")
    return author


@author_router.post('/delete/')
@role_req((Role.ADMIN, Role.S_ADMIN, ))
async def delete(author_id: int,
                 user_id=Depends(require_user), rep: Repository = Depends(get_rep)):
    linked_books = await rep.author_book.count_links_left(author_id)
    if linked_books:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=f'Can not delete author, '
                                                         f'because there are {linked_books} links to books')
    res = await rep.author.delete_data(author_id)
    if res is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Error')
    message = f"Author with id={author_id} deleted"
    logger.debug(f"{message} by user_id={user_id}")
    return {"detail": message}


@author_router.post('/create_link_book/')
@role_req((Role.ADMIN, Role.S_ADMIN, ))
async def create_link_book(author_id: int, book_id: int,
                           user_id=Depends(require_user), rep: Repository = Depends(get_rep)):
    res = await rep.author_book.create_link(author_id, book_id)
    if res is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail='Error')
    message = f"Link Author with id={author_id} to Book with id={book_id} created"
    logger.debug(f"{message} by user_id={user_id}")
    return {"detail": message}


@author_router.post('/delete_link_book/')
@role_req((Role.ADMIN, Role.S_ADMIN, ))
async def delete_link_book(author_id: int, book_id: int,
                             user_id=Depends(require_user), rep: Repository = Depends(get_rep)):
    res = await rep.author_book.delete_one_link(author_id, book_id)
    if res == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Error')
    message = f"Link Author with id={author_id} to Book with id={book_id} deleted"
    logger.debug(f"{message} by user_id={user_id}")
    return {"detail": message}


@author_router.post('/delete_all_links_book/')
@role_req((Role.ADMIN, Role.S_ADMIN, ))
async def delete_all_links_author(author_id: int,
                             user_id=Depends(require_user), rep: Repository = Depends(get_rep)):
    res = await rep.author_book.delete_all_left_links(author_id)
    if res == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Error')
    message = f"{res} links Author to Book with Author id={author_id} deleted"
    logger.debug(f"{message} by user_id={user_id}")
    return {"detail": message}


# книги автора
@author_router.get('/get_books/', response_model=List[BookDB])
async def get_books(author_id: int,
                    item_start: int = 0, item_end: int = 10,
                    rep: Repository = Depends(get_rep)):
    res = await rep.author.get_books(author_id, item_start, item_end)
    if len(res) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Error')
    return [r.to_schema() for r in res]

# жанры автора
@author_router.get('/get_genres/', response_model=List[GenreDB])
async def get_genres(author_id: int,
                     item_start: int = 0, item_end: int = 10,
                     rep: Repository = Depends(get_rep)):
    res = await rep.author.get_genres(author_id, item_start, item_end)
    if len(res) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Error')
    return [r.to_schema() for r in res]

# пользователи читающие/читавшие автора
@author_router.get('/get_users/', response_model=List[UserDBPublic])
@role_req((Role.ADMIN, Role.S_ADMIN, ))
async def get_users(author_id: int, returned: bool,
                    item_start: int = 0, item_end: int = 10,
                    user_id=Depends(require_user), rep: Repository = Depends(get_rep)):
    res = await rep.author.get_users(author_id, returned, item_start, item_end)
    if len(res) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Error')
    return [r.to_schema_public() for r in res]