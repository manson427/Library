from sqlalchemy import String, Integer, Date, Boolean, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date, timedelta
from app.db.models.base import Base
from typing import List
from app.api.schemas.all import (BookDB, BookWithUsersDB, UserBookDB, UserBookWithBookDB,
                                 AuthorDB, GenreDB, UserDB, UserDBPublic, UserWithBooksDB, UserWithBooksBookDB)

# TODO: id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)


class AuthorBook(Base):
    __tablename__ = 'author_book'

    left_id: Mapped[int] = mapped_column(ForeignKey("authors.id"), primary_key=True)
    right_id: Mapped[int] = mapped_column(ForeignKey("books.id"), primary_key=True)

    author: Mapped["Author"] = relationship(back_populates="books")
    book: Mapped["Book"] = relationship(back_populates="authors")


class GenreBook(Base):
    __tablename__ = 'genre_book'

    left_id: Mapped[int] = mapped_column(ForeignKey("genres.id"), primary_key=True)
    right_id: Mapped[int] = mapped_column(ForeignKey("books.id"), primary_key=True)

    genre: Mapped["Genre"] = relationship(back_populates="books")
    book: Mapped["Book"] = relationship(back_populates="genres")


class UserBook(Base):
    __tablename__ = 'user_book'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)

    left_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    right_id: Mapped[int] = mapped_column(ForeignKey("books.id"))

    get_at: Mapped[date] = mapped_column(Date, nullable=False,
                                              server_default=func.now())
    must_return_at: Mapped[date] = mapped_column(Date, nullable=False,
                                               server_default=func.now() + timedelta(days=14))
    returned_at: Mapped[date] = mapped_column(Date, nullable=True)
    returned: Mapped[bool] = mapped_column(Boolean, default=False)

    user: Mapped["User"] = relationship(back_populates="books")
    book: Mapped["Book"] = relationship(back_populates="users")

    def to_schema(self) -> UserBookDB:
        return UserBookDB(
            id=self.id,
            left_id=self.left_id,
            right_id=self.right_id,
            get_at=self.get_at,
            must_return_at=self.must_return_at,
            returned_at=self.returned_at,
            returned=self.returned,
        )

    def to_schema_with_book(self) -> UserBookWithBookDB:
        return UserBookWithBookDB(
            id=self.id,
            left_id=self.left_id,
            right_id=self.right_id,
            get_at=self.get_at,
            must_return_at=self.must_return_at,
            returned_at=self.returned_at,
            returned=self.returned,
            book=Book.to_schema(self.book)
        )


class Author(Base):
    __tablename__ = 'authors'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    books: Mapped[List["AuthorBook"]] = relationship(back_populates='author')
    name: Mapped[str] = mapped_column(String, nullable=False)
    biography: Mapped[str] = mapped_column(String, nullable=False)
    born: Mapped[date] = mapped_column(Date, nullable=False)

    def to_schema(self) -> AuthorDB:
        return AuthorDB(
            id=self.id,
            name=self.name,
            biography=self.biography,
            born=self.born,
        )


class Genre(Base):
    __tablename__ = 'genres'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    books: Mapped[List["GenreBook"]] = relationship(back_populates='genre')
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)

    def to_schema(self) -> GenreDB:
        return GenreDB(
            id=self.id,
            name=self.name,
            description=self.description,
        )


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False)
    role_id: Mapped[int] = mapped_column(Integer, default=0)
    born: Mapped[date] = mapped_column(Date, nullable=False)
    verified: Mapped[bool] = mapped_column(Boolean, default=False)
    refresh_token: Mapped[str] = mapped_column(String, nullable=True)
    verify_code: Mapped[str] = mapped_column(String, nullable=True)
    reset_code: Mapped[str] = mapped_column(String, nullable=True)
    books: Mapped[List["UserBook"]] = relationship(back_populates='user')

    def to_schema(self) -> UserDB:
        return UserDB(
            id=self.id,
            name=self.name,
            hashed_password=self.hashed_password,
            email=self.email,
            role_id=self.role_id,
            born=self.born,
            verified=self.verified,
            refresh_token=self.refresh_token,
            verify_code=self.verify_code,
            reset_code=self.reset_code,
        )

    def to_schema_public(self) -> UserDBPublic:
        return UserDBPublic(
            id=self.id,
            name=self.name,
            email=self.email,
            role_id=self.role_id,
            born=self.born,
            verified=self.verified,
        )

    def to_schema_with_books(self) -> UserWithBooksDB:
        return UserWithBooksDB(
            id=self.id,
            name=self.name,
            email=self.email,
            role_id=self.role_id,
            born=self.born,
            verified=self.verified,
            books=[UserBook.to_schema(u) for u in self.books]
        )

    def to_schema_with_books_book(self) -> UserWithBooksBookDB:
        return UserWithBooksBookDB(
            id=self.id,
            name=self.name,
            email=self.email,
            role_id=self.role_id,
            born=self.born,
            verified=self.verified,
            books=[UserBook.to_schema_with_book(u) for u in self.books]
        )


class Book(Base):
    __tablename__ = 'books'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    publish_year: Mapped[int] = mapped_column(Integer, nullable=False)
    authors: Mapped[List["AuthorBook"]] = relationship(back_populates='book')
    genres: Mapped[List["GenreBook"]] = relationship(back_populates='book')
    users: Mapped[List["UserBook"]] = relationship(back_populates='book')
    amount: Mapped[int] = mapped_column(Integer, nullable=True)

    def to_schema(self) -> BookDB:
        return BookDB(
            id=self.id,
            name=self.name,
            description=self.description,
            publish_year=self.publish_year,
            amount=self.amount,)

    def to_schema_with_users(self) -> BookWithUsersDB:
        return BookWithUsersDB(
            id=self.id,
            name=self.name,
            description=self.description,
            publish_year=self.publish_year,
            users=[UserBook.to_schema(u) for u in self.users],
            amount=self.amount,)