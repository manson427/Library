from fastapi import (
    APIRouter, Depends, HTTPException, Response, status, Request, Body, Path,
    Cookie
)

from app.api.schemas.all import GenreCreate, GenreDB, AuthorDB, UserWithBooksBookDB
from typing import List
from app.db.database import get_rep, Repository
from app.api.utils.security import get_password_hash, create_token, require_user, verify_password
from app.api.roles import Role, role_req
from app.log.logger import logger


genre_router = APIRouter(
    prefix="/genre",
    tags=["Genre"]
)


@genre_router.get('/get_one/', response_model=GenreDB)
async def get_one(genre_id: int,
                  rep: Repository = Depends(get_rep)):
    res = await rep.genre.get_one(genre_id)
    if res is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Error')
    return res.to_schema()


@genre_router.get('/get/', response_model=List[GenreDB])
async def get(item_start: int = 0, item_end: int = 10,
              rep: Repository = Depends(get_rep)):
    res = await rep.genre.get(item_start, item_end)
    if len(res) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Error')
    return [r.to_schema() for r in res]


@genre_router.get('/get_like/', response_model=List[GenreDB])
async def get_like(phrase: str,
                   item_start: int = 0, item_end: int = 10,
                   rep: Repository = Depends(get_rep)):
    res = await rep.genre.get_names_like(phrase, item_start, item_end)
    if len(res) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Error')
    return [r.to_schema() for r in res]


@genre_router.post('/create/', response_model=GenreDB)
@role_req((Role.ADMIN, Role.S_ADMIN, ))
async def create(genre: GenreCreate,
                 user_id=Depends(require_user), rep: Repository = Depends(get_rep)):
    res = await rep.genre.create(genre.model_dump())
    if res is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail='Error')
    genre = res.to_schema()
    logger.debug(f"Genre with id={genre.id} created")
    return genre


@genre_router.post('/delete/')
@role_req((Role.ADMIN, Role.S_ADMIN, ))
async def delete(genre_id: int,
                 user_id=Depends(require_user), rep: Repository = Depends(get_rep)):
    linked_books = await rep.genre_book.count_links_left(genre_id)
    if linked_books:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=f'Can not delete genre, '
                                                         f'because there are {linked_books} links to books')
    res = await rep.genre.delete_data(genre_id)
    if res is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Error')
    message = f"Genre with id={genre_id} deleted"
    logger.debug(f"{message} by user_id={user_id}")
    return {"detail": message}


@genre_router.post('/create_link_book/')
@role_req((Role.ADMIN, Role.S_ADMIN, ))
async def create_link_book(genre_id: int, book_id: int,
                           user_id=Depends(require_user), rep: Repository = Depends(get_rep)):
    res = await rep.genre_book.create_link(genre_id, book_id)
    if res is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail='Error')
    message = f"Link Genre with id={genre_id} to Book with id={book_id} created"
    logger.debug(f"{message} by user_id={user_id}")
    return {"detail": message}


@genre_router.post('/delete_link_book/')
@role_req((Role.ADMIN, Role.S_ADMIN, ))
async def delete_link_book(genre_id: int, book_id: int,
                            user_id=Depends(require_user), rep: Repository = Depends(get_rep)):
    res = await rep.genre_book.delete_one_link(genre_id, book_id)
    if res == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Error')
    message = f"Link Genre with id={genre_id} to Book with id={book_id} deleted"
    logger.debug(f"{message} by user_id={user_id}")
    return {"detail": message}


@genre_router.post('/delete_all_links_book/')
@role_req((Role.ADMIN, Role.S_ADMIN, ))
async def delete_all_links_genre(genre_id: int,
                            user_id=Depends(require_user), rep: Repository = Depends(get_rep)):
    res = await rep.genre_book.delete_all_left_links(genre_id)
    if res == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Error')
    message = f"{res} links Genre to Book with Genre id={genre_id} deleted"
    logger.debug(f"{message} by user_id={user_id}")
    return {"detail": message}


# книги жанра
@genre_router.get('/get_books/', response_model=List[GenreDB])
async def get_books(genre_id: int,
                    item_start: int = 0, item_end: int = 10,
                    rep: Repository = Depends(get_rep)):
    res = await rep.genre.get_books(genre_id, item_start, item_end)
    if len(res) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Error')
    return [r.to_schema() for r in res]


# авторы жанра
@genre_router.get('/get_authors/', response_model=List[AuthorDB])
async def get_authors(genre_id: int,
                      item_start: int = 0, item_end: int = 10,
                      rep: Repository = Depends(get_rep)):
    res = await rep.genre.get_authors(genre_id, item_start, item_end)
    if len(res) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Error')
    return [r.to_schema() for r in res]


# пользователи читающие/читавшие жанр
@genre_router.get('/get_users/', response_model=List[UserWithBooksBookDB])
@role_req((Role.ADMIN, Role.S_ADMIN, ))
async def get_users(genre_id: int, returned: bool,
                    item_start: int = 0, item_end: int = 10,
                    user_id=Depends(require_user), rep: Repository = Depends(get_rep)):
    res = await rep.genre.get_users(genre_id, returned, item_start, item_end)
    if len(res) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Error')
    return [r.to_schema_with_books_book() for r in res]
