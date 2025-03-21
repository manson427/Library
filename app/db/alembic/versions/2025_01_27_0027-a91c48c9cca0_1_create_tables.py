"""1_create_tables

Revision ID: a91c48c9cca0
Revises: 
Create Date: 2025-01-27 00:27:31.553366

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a91c48c9cca0'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('authors',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('biography', sa.String(), nullable=False),
    sa.Column('born', sa.Date(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('books',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('publish_year', sa.Integer(), nullable=False),
    sa.Column('amount', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('genres',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('hashed_password', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('role_id', sa.Integer(), nullable=False),
    sa.Column('born', sa.Date(), nullable=False),
    sa.Column('verified', sa.Boolean(), nullable=False),
    sa.Column('refresh_token', sa.String(), nullable=True),
    sa.Column('verify_code', sa.String(), nullable=True),
    sa.Column('reset_code', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('author_book',
    sa.Column('left_id', sa.Integer(), nullable=False),
    sa.Column('right_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['left_id'], ['authors.id'], ),
    sa.ForeignKeyConstraint(['right_id'], ['books.id'], ),
    sa.PrimaryKeyConstraint('left_id', 'right_id')
    )
    op.create_table('genre_book',
    sa.Column('left_id', sa.Integer(), nullable=False),
    sa.Column('right_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['left_id'], ['genres.id'], ),
    sa.ForeignKeyConstraint(['right_id'], ['books.id'], ),
    sa.PrimaryKeyConstraint('left_id', 'right_id')
    )
    op.create_table('user_book',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('left_id', sa.Integer(), nullable=False),
    sa.Column('right_id', sa.Integer(), nullable=False),
    sa.Column('get_at', sa.Date(), server_default=sa.text('now()'), nullable=False),
    sa.Column('must_return_at', sa.Date(), server_default=sa.text('now() + make_interval(secs=>1209600.0)'), nullable=False),
    sa.Column('returned_at', sa.Date(), nullable=True),
    sa.Column('returned', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['left_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['right_id'], ['books.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_book')
    op.drop_table('genre_book')
    op.drop_table('author_book')
    op.drop_table('users')
    op.drop_table('genres')
    op.drop_table('books')
    op.drop_table('authors')
    # ### end Alembic commands ###
