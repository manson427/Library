from fastapi import (
    APIRouter, Depends, HTTPException, Response, status, Request, Body, Path,
    Cookie
)

from datetime import date
from app.api.schemas.all import AuthorDB, UserData, BookWithUsersDB, BookDB, UserDB, UserDBPublic

from typing import List
from app.config import settings

from app.db.database import get_rep, Repository

from app.api.utils.security import require_user
from app.log.logger import logger


user_router = APIRouter(
    prefix="/user",
    tags=["User"]
)


@user_router.get('/get_me/', response_model=UserDBPublic)
async def get_me(user_id = Depends(require_user), rep: Repository = Depends(get_rep)):
    res = await rep.user.get_one(user_id)
    if res is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Error')
    return res.to_schema_public()


@user_router.post('/update_me/', response_model=UserDBPublic)
async def update_me(user_data: UserData,
                    user_id = Depends(require_user), rep: Repository = Depends(get_rep)):
    res = await rep.user.update(user_id, **user_data.model_dump())
    return res.to_schema_public()


@user_router.post('/delete/')
async def delete(user_id=Depends(require_user), rep: Repository = Depends(get_rep)):
    books_out = await rep.user.get_books(user_id, returned=False, item_start=0, item_end=1)
    if books_out:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=f'Can not delete user, '
                                                         f'because there are {len(books_out)} taken books')
    linked_books = await rep.user_book.count_links_left(user_id)
    if linked_books:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=f'Can not delete user, '
                                                         f'because there are {linked_books} returned books')
    res = await rep.user.delete_data(user_id)
    if res is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Error')
    user = res.to_schema_public()
    message = f"User '{user.name}' with id={user.id} deleted"
    logger.debug(f"{message} by himself")
    return {'detail': message}


@user_router.post('/delete_all_links_book/')
async def delete_all_links_book(user_id=Depends(require_user), rep: Repository = Depends(get_rep)):
    res = await rep.user_book.delete_all_left_links_returned(user_id, True)
    if res == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Error')
    message = f"{res} links User to Book with User id={user_id} deleted"
    logger.debug(f"{message} himself")
    return {"detail": message}


# получение книги
@user_router.post('/take_book/')
async def take_book(book_id: int,
                    user_id = Depends(require_user), rep: Repository = Depends(get_rep)):
    max_amount: int = settings.MAX_AMOUNT
    user_s__books = await rep.user.get_books(user_id, returned=False, item_start=0, item_end=max_amount)
    user_s__books_schema = [b.to_schema_with_users() for b in user_s__books]
    if any([b for b in user_s__books_schema if b.id == book_id]):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail='You already have same book')
    if len(user_s__books_schema) >= max_amount:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail='You have too many books')
    if any([b.users[0].must_return_at < date.today() and
            b.users[0].returned == False
            for b in user_s__books_schema]):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail='First, you must receive overdue book')

    book = await rep.book.get_one(book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Error')
    if book.to_schema().amount == 0:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail='Not enough copies of the book')

    user = await rep.user.get_one(user_id)
    if not (user_book := await rep.user.user_take_book(user, book)):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Internal error')

    message = f"take Book with id={book_id}"
    logger.debug(f"User with id={user_id} {message}")
    return {"detail": f"You successfully {message}",
            "book": book.to_schema(),
            "must_returned_at": user_book.must_return_at}


# возврат книги
@user_router.post('/return_book/')
async def return_book(book_id: int,
                      user_id = Depends(require_user), rep: Repository = Depends(get_rep)):
    max_amount: int = settings.MAX_AMOUNT
    book = await rep.user.get_book(user_id, book_id, item_start=0, item_end=max_amount)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail='You have not this book')
    user_book = await rep.user_book.get_link(user_id, book_id, False)
    if not user_book:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Internal error')
    book_schema: BookDB = await rep.user.user_return_book(link=user_book, book=book)
    message = f"return Book with id={book_schema.id}"
    logger.debug(f"User with id={user_id} {message}")
    return {"detail": f"You successfully {message}",
            "book": book_schema}


# книги пользователя читаемые/прочитанные
@user_router.get('/get_my_books/', response_model=List[BookDB])
async def get_my_books(returned: bool,
                       item_start: int = 0, item_end: int = 10,
                       user_id = Depends(require_user), rep: Repository = Depends(get_rep)):
    res = await rep.user.get_books(user_id, returned, item_start, item_end)
    if len(res) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Error')
    return [r.to_schema() for r in res]


# жанры книг пользователя читаемые/прочитанные
@user_router.get('/get_my_genres/', response_model=List[BookWithUsersDB])
async def get_my_genres(returned: bool,
                        item_start: int = 0, item_end: int = 10,
                        user_id=Depends(require_user), rep: Repository = Depends(get_rep)):
    res = await rep.user.get_genres(user_id, returned, item_start, item_end)
    if len(res) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Error')
    return [r.to_schema_with_users() for r in res]


# авторы книг пользователя читаемые/прочитанные
@user_router.get('/get_my_authors/', response_model=List[AuthorDB])
async def get_my_authors(returned: bool,
                         item_start: int = 0, item_end: int = 10,
                         user_id=Depends(require_user), rep: Repository = Depends(get_rep)):
    res = await rep.user.get_authors(user_id, returned, item_start, item_end)
    if len(res) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Error')
    return [r.to_schema() for r in res]

