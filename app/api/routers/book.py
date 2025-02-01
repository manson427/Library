from fastapi import (
    APIRouter, Depends, HTTPException, Response, status, Request, Body, Path,
    Cookie
)
from app.api.schemas.all import BookCreate, BookDB, UserWithBooksDB, GenreDB, AuthorDB
from typing import List
from app.db.database import get_rep, Repository
from app.api.utils.security import require_user
from app.api.roles import Role, role_req
from app.log.logger import logger


book_router = APIRouter(
    prefix="/book",
    tags=["Book"]
)

@book_router.get('/get_one/', response_model=BookDB)
async def get_one(book_id: int,
                  rep: Repository = Depends(get_rep)):
    res = await rep.book.get_one(book_id)
    if res is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Error')
    return res.to_schema()


@book_router.get('/get/', response_model=List[BookDB])
async def get(item_start: int = 0, item_end: int = 10,
              rep: Repository = Depends(get_rep)):
    res = await rep.book.get(item_start, item_end)
    if len(res) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Error')
    return [r.to_schema() for r in res]


@book_router.get('/get_like/', response_model=List[BookDB])
async def get_like(phrase: str,
                   item_start: int = 0, item_end: int = 10,
                   rep: Repository = Depends(get_rep)):
    res = await rep.book.get_names_like(phrase, item_start, item_end)
    if len(res) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Error')
    return [r.to_schema() for r in res]


@book_router.post('/create/', response_model=BookDB)
@role_req((Role.ADMIN, Role.S_ADMIN, ))
async def create(book: BookCreate,
                 user_id=Depends(require_user), rep: Repository = Depends(get_rep)):
    res = await rep.book.create(book.model_dump())
    if res is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail='Error')
    book = res.to_schema()
    logger.debug(f"Book with id={book.id} created")
    return book


@book_router.post('/delete/')
@role_req((Role.ADMIN, Role.S_ADMIN, ))
async def delete(book_id: int,
                 user_id=Depends(require_user), rep: Repository = Depends(get_rep)):
    linked_authors = await rep.author_book.count_links_right(book_id)
    if linked_authors:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=f'Can not delete book, '
                                                         f'because there are {linked_authors} links to authors')

    linked_genres = await rep.genre_book.count_links_right(book_id)
    if linked_genres:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=f'Can not delete book, '
                                                         f'because there are {linked_genres} links to genres')

    books_out = await rep.book.get_users(book_id, returned=False, item_start=0, item_end=1)
    if books_out:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=f'Can not delete book, '
                                                         f'because there are {len(books_out)} copies out')

    linked_users = await rep.user_book.count_links_right(book_id)
    if linked_users:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=f'Can not delete book, '
                                                         f'because there are {linked_users} links to users')


    res = await rep.book.delete_data(book_id)
    if res is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Error')
    message = f"Book with id={book_id} deleted"
    logger.debug(f"{message} by user_id={user_id}")
    return {"detail": message}


@book_router.post('/create_link_author/')
@role_req((Role.ADMIN, Role.S_ADMIN, ))
async def create_link_author(author_id: int, book_id: int,
                             user_id=Depends(require_user), rep: Repository = Depends(get_rep)):
    res = await rep.author_book.create_link(author_id, book_id)
    if res is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail='Error')
    message = f"Link Author with id={author_id} to Book with id={book_id} created"
    logger.debug(f"{message} by user_id={user_id}")
    return {"detail": message}


@book_router.post('/delete_link_author/')
@role_req((Role.ADMIN, Role.S_ADMIN, ))
async def delete_link_author(author_id: int, book_id: int,
                             user_id=Depends(require_user), rep: Repository = Depends(get_rep)):
    res = await rep.author_book.delete_one_link(author_id, book_id)
    if res == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Error')
    message = f"Link Author with id={author_id} to Book with id={book_id} deleted"
    logger.debug(f"{message} by user_id={user_id}")
    return {"detail": message}


@book_router.post('/delete_all_links_author/')
@role_req((Role.ADMIN, Role.S_ADMIN, ))
async def delete_all_links_author(book_id: int,
                             user_id=Depends(require_user), rep: Repository = Depends(get_rep)):
    res = await rep.author_book.delete_all_right_links(book_id)
    if res == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Error')
    message = f"{res} links Author to Book with Book id={book_id} deleted"
    logger.debug(f"{message} by user_id={user_id}")
    return {"detail": message}


@book_router.post('/create_link_genre/')
@role_req((Role.ADMIN, Role.S_ADMIN, ))
async def create_link_genre(genre_id: int, book_id: int,
                            user_id=Depends(require_user), rep: Repository = Depends(get_rep)):
    res = await rep.genre_book.create_link(genre_id, book_id)
    if res is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail='Error')
    message = f"Link Genre with id={genre_id} to Book with id={book_id} created"
    logger.debug(f"{message} by user_id={user_id}")
    return {"detail": message}


@book_router.post('/delete_link_genre/')
@role_req((Role.ADMIN, Role.S_ADMIN, ))
async def delete_link_genre(genre_id: int, book_id: int,
                            user_id=Depends(require_user), rep: Repository = Depends(get_rep)):
    res = await rep.genre_book.delete_one_link(genre_id, book_id)
    if res == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Error')
    message = f"Link Genre with id={genre_id} to Book with id={book_id} deleted"
    logger.debug(f"{message} by user_id={user_id}")
    return {"detail": message}


@book_router.post('/delete_all_links_genre/')
@role_req((Role.ADMIN, Role.S_ADMIN, ))
async def delete_all_links_genre(book_id: int,
                            user_id=Depends(require_user), rep: Repository = Depends(get_rep)):
    res = await rep.genre_book.delete_all_right_links(book_id)
    if res == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Error')
    message = f"{res} links Genre to Book with Book id={book_id} deleted"
    logger.debug(f"{message} by user_id={user_id}")
    return {"detail": message}


@book_router.post('/delete_all_links_returned_books/')
@role_req((Role.ADMIN, Role.S_ADMIN, ))
async def delete_all_links_returned_books(book_id: int,
                            user_id=Depends(require_user), rep: Repository = Depends(get_rep)):
    res = await rep.user_book.delete_all_right_links_returned(book_id, True)
    if res == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Error')
    message = f"{res} links User to Book with Book id={book_id} deleted"
    logger.debug(f"{message} by user_id={user_id}")
    return {"detail": message}


# авторы книги
@book_router.get('/get_authors/', response_model=List[AuthorDB])
async def get_authors(book_id: int,
                      item_start: int = 0, item_end: int = 10,
                      rep: Repository = Depends(get_rep)):
    res = await rep.book.get_authors(book_id, item_start, item_end)
    if len(res) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Error')
    return [r.to_schema() for r in res]


# жанры книги
@book_router.get('/get_genres/', response_model=List[GenreDB])
async def get_genres(book_id: int,
                     item_start: int = 0, item_end: int = 10,
                     rep: Repository = Depends(get_rep)):
    res = await rep.book.get_genres(book_id, item_start, item_end)
    if len(res) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Error')
    return [r.to_schema() for r in res]


# пользователи читающие/читавшие книгу
@book_router.get('/get_users/', response_model=List[UserWithBooksDB])
@role_req((Role.ADMIN, Role.S_ADMIN, ))
async def get_users(book_id: int, returned: bool,
                    item_start: int = 0, item_end: int = 10,
                    user_id = Depends(require_user), rep: Repository = Depends(get_rep)):
    res = await rep.book.get_users(book_id, returned, item_start, item_end)
    if len(res) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Error')
    return [r.to_schema_with_books() for r in res]

