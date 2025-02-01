from app.db.models.all import AuthorBook, GenreBook, UserBook, Author, Genre, Book, User
from app.api.schemas.all import BookDB, UserBookDB
from app.db.repositories.base_repository import RepositoryData, RepositoryLink
from sqlalchemy import select, and_, delete
from sqlalchemy.orm import selectinload
from typing import List
from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession


class AuthorRepository(RepositoryData):
    Model = Author

    # Книги автора
    async def get_books(self, author_id: int,
                        item_start: int, item_end: int
                        ) -> List[Book]:
        stmt = (select(Book).
                join(Book.authors).join(AuthorBook.author).
                where(Author.id == author_id).
                slice(item_start, item_end))
        res = await self.session.execute(stmt)
        books = res.scalars().unique().all()
        return list(books)

    # Жанры автора
    async def get_genres(self, author_id: int,
                         item_start: int, item_end: int
                         ) -> List[Genre]:
        stmt = (select(Genre).
                join(Genre.books).join(GenreBook.book).
                join(Book.authors).join(AuthorBook.author).
                where(Author.id == author_id).distinct().
                order_by(Genre.name).
                slice(item_start, item_end))
        res = await self.session.execute(stmt)
        genres = res.scalars().unique().all()
        return list(genres)

    # Читатели, читающие/прочитавшие книги автора
    async def get_users(self, author_id: int, returned: bool,
                        item_start: int, item_end: int
                        ) -> List[User]:
        stmt = (select(User).
                join(User.books).join(UserBook.book).where(UserBook.returned == returned).
                join(Book.authors).join(AuthorBook.author).
                where(Author.id == author_id).distinct().
                order_by(User.name).
                slice(item_start, item_end))
        res = await self.session.execute(stmt)
        users = res.scalars().unique().all()
        return list(users)


class GenreRepository(RepositoryData):
    Model = Genre

    # Книги жанра
    async def get_books(self, genre_id: int,
                        item_start: int, item_end: int
                        ) -> List[Book]:
        stmt = (select(Book).
                join(Book.genres).join(GenreBook.genre).
                where(Genre.id == genre_id).
                slice(item_start, item_end))
        res = await self.session.execute(stmt)
        books = res.scalars().unique().all()
        return list(books)

    # Авторы написавшие книги жанра
    async def get_authors(self, genre_id: int,
                          item_start: int, item_end: int
                          ) -> List[Author]:
        stmt = (select(Author).
                join(Author.books).join(AuthorBook.book).
                join(Book.genres).join(GenreBook.genre).
                where(Genre.id == genre_id).
                distinct().
                order_by(Author.name).
                slice(item_start, item_end))
        res = await self.session.execute(stmt)
        authors = res.scalars().unique().all()
        return list(authors)

    # Читатели, читающие/прочитавшие книги жанра
    async def get_users(self, genre_id: int, returned: bool,
                        item_start: int, item_end: int
                        ) -> List[User]:
        stmt = (select(User).
                join(User.books).join(UserBook.book).where(UserBook.returned == returned).
                join(Book.genres).join(GenreBook.genre).
                where(Genre.id == genre_id).distinct().
                options(selectinload(User.books.and_(UserBook.returned == returned)).subqueryload(UserBook.book)).
                order_by(User.name).
                slice(item_start, item_end))
        res = await self.session.execute(stmt)
        users = res.scalars().unique().all()
        return list(users)

    # не используется
    # async def delete_links_and_data_orm(self, genre_id: int):
    #     stmt = select(Genre).where(Author.id == genre_id).options(selectinload(Genre.books))
    #     res = await self.session.execute(stmt)
    #     data = res.scalars().unique().one()
    #     n = len(data.books)
    #     for a in data.books:
    #         await self.session.delete(a)
    #     await self.session.delete(data)
    #     await self.session.commit()
    #     return n


class UserRepository(RepositoryData):
    Model = User

    # Книга читателя несданная
    async def get_book(self, user_id: int, book_id: int,
                        item_start: int, item_end: int
                        ) -> Book:
        stmt = (select(Book).
                join(Book.users).
                join(UserBook.user).
                where(and_(UserBook.returned == False,
                           User.id == user_id,
                           Book.id == book_id)).
                order_by(Book.name).
                slice(item_start, item_end))
        res = await self.session.execute(stmt)
        book = res.scalars().unique().first()
        return book

    # Книги читателя читаемые/прочитанные
    async def get_books(self, user_id: int, returned: bool,
                        item_start: int, item_end: int
                        ) -> List[Book]:
        stmt = (select(Book).
                join(Book.users).
                join(UserBook.user).
                where(and_(UserBook.returned == returned,
                            User.id == user_id)).
                options(selectinload(Book.users.and_(UserBook.returned == returned))).
                order_by(Book.name).
                slice(item_start, item_end))
        res = await self.session.execute(stmt)
        books = res.scalars().unique().all()
        return list(books)

    # Жанры книг читаемых / прочитанных (сданных) читателем
    async def get_genres(self, user_id: int, returned: bool,
                         item_start: int, item_end: int
                         ) -> List[Genre]:
        stmt = (select(Genre).
                join(Genre.books).join(GenreBook.book).
                join(Book.users).join(UserBook.user).
                where(and_(
                        UserBook.returned == returned,
                        User.id == user_id
                    )
                ).distinct().
                order_by(Genre.name).
                slice(item_start, item_end))
        res = await self.session.execute(stmt)
        genres = res.scalars().unique().all()
        return list(genres)

    # Авторы книг читаемых / прочитанных (сданных) читателем
    async def get_authors(self, user_id: int, returned: bool,
                          item_start: int, item_end: int
                          ) -> List[Author]:
        stmt = (select(Author).
                join(Author.books).join(AuthorBook.book).
                join(Book.users).join(UserBook.user).
                where(and_(
                        UserBook.returned == returned,
                        User.id == user_id)).
                distinct().
                order_by(Author.name).
                slice(item_start, item_end))
        res = await self.session.execute(stmt)
        authors = res.scalars().unique().all()
        return list(authors)

    # Читатели задержавшие сдачу книг, уже сдавшие / до сих пор не сдавшие
    async def get_overdue(self, returned: bool,
                          item_start: int, item_end: int
                          ) -> List[User]:
        stmt = (select(User).
                join(User.books).join(UserBook.book).
                where(and_(
                        UserBook.returned == returned,
                        (UserBook.returned_at if returned else date.today()) > UserBook.must_return_at,
                    )).
                options(selectinload(User.books.and_(UserBook.returned == returned)).subqueryload(UserBook.book)).
                order_by(User.name).
                slice(item_start, item_end))
        res = await self.session.execute(stmt)
        users = res.scalars().unique().all()
        return list(users)

    # Получение книги (создать связь, уменьшить ко-во книг на складе на 1)
    async def user_take_book(self, user: User, book: Book) -> UserBookDB:
        book.amount -= 1
        link = UserBook(book=book, user=user)
        # .append(link)
        self.session.add_all([book, link])
        await self.session.commit()
        return link.to_schema()

    # Получение книги (для связи установить флаг сдана и дату сдачи, увеличить кол-во книг на складе на 1)
    async def user_return_book(self, link: UserBook, book: Book) -> BookDB:
        link.returned = True
        link.returned_at = date.today()
        book.amount += 1
        self.session.add_all([link, book])
        await self.session.commit()
        return book.to_schema()


class BookRepository(RepositoryData):
    Model = Book

    # Авторы книги
    async def get_authors(self, book_id: int,
                          item_start: int, item_end: int
                          ) -> List[Author]:
        stmt = (select(Author).
                join(Author.books).join(AuthorBook.book).
                where(Book.id == book_id).
                distinct().
                slice(item_start, item_end))
        res = await self.session.execute(stmt)
        authors = res.scalars().unique().all()
        return list(authors)

    # Жанры книги
    async def get_genres(self, book_id: int,
                         item_start: int, item_end: int
                         ) -> List[Genre]:
        stmt = (select(Genre).
                join(Genre.books).join(GenreBook.book).
                where(Book.id == book_id).
                distinct().
                slice(item_start, item_end))
        res = await self.session.execute(stmt)
        genres = res.scalars().unique().all()
        return list(genres)

    # Читатели, читающие/прочитавшие книгу
    async def get_users(self, book_id: int, returned: bool,
                        item_start: int, item_end: int
                        ) -> List[User]:
        stmt = (select(User).
                join(User.books).join(UserBook.book).
                where(and_(
                        UserBook.returned == returned,
                        Book.id == book_id
                    )
                ).
                options(selectinload(User.books.and_(
                        UserBook.returned == returned,
                        UserBook.right_id == book_id)
                    )
                ).
                order_by(User.name).
                slice(item_start, item_end))
        res = await self.session.execute(stmt)
        users = res.scalars().unique().all()
        return list(users)


class AuthorBookRepository(RepositoryLink):
    Model = AuthorBook


class GenreBookRepository(RepositoryLink):
    Model = GenreBook


class UserBookRepository(RepositoryLink):
    Model = UserBook

    async def delete_all_left_links_returned(self, left_id: int, returned: bool) -> int():
        stmt = (delete(UserBook).
                where(and_(
                    UserBook.left_id == left_id),
                    UserBook.returned == returned))
        res = await self.session.execute(stmt)
        await self.session.commit()
        return res.rowcount

    async def delete_all_right_links_returned(self, right_id: int, returned: bool) -> int():
        stmt = (delete(UserBook).
                where(and_(
                    UserBook.right_id == right_id),
                    UserBook.returned == returned))
        res = await self.session.execute(stmt)
        await self.session.commit()
        return res.rowcount


class Repository:
    def __init__(self, session: AsyncSession):
        self.author = AuthorRepository(session)
        self.genre = GenreRepository(session)
        self.user = UserRepository(session)
        self.book = BookRepository(session)
        self.author_book = AuthorBookRepository(session)
        self.genre_book = GenreBookRepository(session)
        self.user_book = UserBookRepository(session)