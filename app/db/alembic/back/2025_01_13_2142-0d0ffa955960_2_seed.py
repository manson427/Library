"""2_seed

Revision ID: 0d0ffa955960
Revises: e86a3e3af5f5
Create Date: 2025-01-13 14:52:40.032842

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from app.config import settings
from app.db.models.all import Author, Book, Genre, User, AuthorBook, GenreBook, UserBook
from app.api.utils.security import get_password_hash

# revision identifiers, used by Alembic.
revision: str = '0d0ffa955960'
down_revision: Union[str, None] = 'a91c48c9cca0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

author_table = sa.inspect(Author).tables[0]
book_table = sa.inspect(Book).tables[0]
genre_table = sa.inspect(Genre).tables[0]
user_table = sa.inspect(User).tables[0]
author_book_table = sa.inspect(AuthorBook).tables[0]
genre_book_table = sa.inspect(GenreBook).tables[0]
user_book_table = sa.inspect(UserBook).tables[0]

authors = [
    {
        "id": 1,
        "name": 'Илья Арнольдович Ильф',
        "biography": 'Русский советский писатель, драматург и сценарист, фотограф, журналист',
        "born": '1897.10.15',
    },
    {
        "id": 2,
        "name": 'Евгений Петрович Петров',
        "biography": 'Русский советский писатель, сценарист и драматург, журналист, военный '
                     'корреспондент. Кавалер ордена Ленина (1939). Член ВКП(б) с 1939 года.',
        "born": '1902.12.30',
    },
    {
        "id": 3,
        "name": 'Лев Николаевич Толстой',
        "biography": 'Один из наиболее известных русских писателей и мыслителей, один из '
                     'величайших в мире писателей-романистов.',
        "born": '1828.09.09',
    },
]
books = [
    {
        "id": 1,
        "name": 'Двенадцать стульев',
        "description": 'Роман Ильи Ильфа и Евгения Петрова, написанный в 1927 году и являющийся '
                       'первой совместной работой соавторов. В 1928 году опубликован в '
                       'художественно-литературном журнале «Тридцать дней» (№ 1—7); в том же году '
                       'издан отдельной книгой. В основе сюжета — поиски бриллиантов, спрятанных '
                       'в одном из двенадцати стульев мадам Петуховой, однако история, изложенная '
                       'в произведении, не ограничена рамками приключенческого жанра: в ней, по '
                       'мнению исследователей, дан «глобальный образ эпохи».',
        "publish_year": 1928,
        "amount": 5,
    },
    {
        "id": 2,
        "name": 'Война и мир',
        "description": 'Роман-эпопея Льва Николаевича Толстого, описывающий русское общество '
                       'в эпоху войн против Наполеона в 1805—1812 годах. Эпилог романа доводит '
                       'повествование до 1820 года',
        "publish_year": 1865,
        "amount": 6,
    },
]
genres = [
    {
        "id": 1,
        "name": 'Роман',
        "description": 'Литературный жанр, чаще прозаический, зародившийся в Средние века '
                       'у романских народов, как рассказ на народном языке и ныне превратившийся '
                       'в самый распространённый вид эпической литературы, изображающий жизнь '
                       'персонажа с её волнующими страстями, борьбой, социальными '
                       'противоречиями и стремлениями к идеалу. Будучи развёрнутым повествованием '
                       'о жизни и развитии личности главного героя (героев) в кризисный, '
                       'нестандартный период его жизни, отличается от повести объёмом, сложностью '
                       'содержания и более широким захватом описываемых явлений',
    },
    {
        "id": 2,
        "name": 'Эпопея',
        "description": 'Обширное эпическое повествование в стихах или прозе о выдающихся '
                       'национально-исторических событиях. В переносном смысле: сложная, '
                       'продолжительная история чего-либо, включающая ряд крупных событий.',
    },
]
users = [
    {
        'name': settings.DEFAULT_USERNAME,
        'hashed_password': get_password_hash(settings.DEFAULT_PASSWORD.get_secret_value()),
        'email': settings.DEFAULT_EMAIL,
        'role_id': 1,
        'born': "2024-12-29",
        'verified': False,
        "refresh_token": None,
        "verify_code": None,
        "reset_code": None,
    },
    {
        'name': 'user1',
        'hashed_password': get_password_hash('user1'),
        'email': settings.DEFAULT_EMAIL,
        'role_id': 1,
        'born': "2024-12-29",
        'verified': False,
        "refresh_token": None,
        "verify_code": None,
        "reset_code": None,
    },
    {
        'name': 'user2',
        'hashed_password': get_password_hash('user2'),
        'email': settings.DEFAULT_EMAIL,
        'role_id': 1,
        'born': "2024-12-29",
        'verified': False,
        "refresh_token": None,
        "verify_code": None,
        "reset_code": None,
    },
]

authors_books = [
    {
        "left_id": 1,
        "right_id": 1,
    },
    {
        "left_id": 2,
        "right_id": 1,
    },
    {
        "left_id": 3,
        "right_id": 2,
    },
]
genres_books = [
    {
        "left_id": 1,
        "right_id": 1,
    },
    {
        "left_id": 1,
        "right_id": 2,
    },
    {
        "left_id": 2,
        "right_id": 2,
    },
]
users_books = [
    { # сдано
        "left_id": '2',
        "right_id": 1,
        "get_at": "2024-11-01",
        "must_return_at": "2024-11-15",
        "returned_at": "2024-11-12",
        "returned": True,
    },
    { # сдано с просрочкой
        "left_id": '3',
        "right_id": 2,
        "get_at": "2024-11-01",
        "must_return_at": "2024-11-15",
        "returned_at": "2024-11-16",
        "returned": True,
    },
    { # не сдано
        "left_id": '2',
        "right_id": 2,
        "get_at": "2025-01-10",
        "must_return_at": "2024-01-24",
        "returned_at": None,
        "returned": False,
    },
    { # не сдано, просрочено
        "left_id": '3',
        "right_id": 1,
        "get_at": "2024-11-01",
        "must_return_at": "2024-11-15",
        "returned_at": None,
        "returned": False,
    },
]

def upgrade() -> None:
    op.bulk_insert(author_table, authors)
    op.bulk_insert(book_table, books)
    op.bulk_insert(genre_table, genres)
    op.bulk_insert(user_table, users)
    op.bulk_insert(author_book_table, authors_books)
    op.bulk_insert(genre_book_table, genres_books)
    op.bulk_insert(user_book_table, users_books)


def downgrade() -> None:
    op.get_bind().execute(author_book_table.delete())
    op.get_bind().execute(genre_book_table.delete())
    op.get_bind().execute(user_book_table.delete())
    op.get_bind().execute(author_table.delete())
    op.get_bind().execute(book_table.delete())
    op.get_bind().execute(genre_table.delete())
    op.get_bind().execute(user_table.delete())
