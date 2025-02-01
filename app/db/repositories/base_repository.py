from abc import ABC, abstractmethod

from sqlalchemy import select, insert, update, delete, and_, func, Sequence, Row
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert
from typing import List


class AbstractRepositoryData(ABC):
    Model = None

    @abstractmethod
    async def create(self, data: dict) -> Model:
        raise NotImplementedError

    @abstractmethod
    async def get_by_name(self, name: str) -> Model:
        raise NotImplementedError

    @abstractmethod
    async def get_one(self, read_id: int) -> Model:
        raise NotImplementedError

    @abstractmethod
    async def get(self, item_start: int, item_end: int) -> List[Model]:
        raise NotImplementedError

    @abstractmethod
    async def get_names_like(self, phrase: str, item_start: int, item_end: int) -> List[Model]:
        raise NotImplementedError

    @abstractmethod
    async def update(self, update_id: int, **kw) -> Model:
        raise NotImplementedError

    @abstractmethod
    async def delete_data(self, delete_id: int) -> Model:
        raise NotImplementedError


class RepositoryData(AbstractRepositoryData):
    Model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: dict) -> Model:
        stmt = insert(self.Model).values(**data).returning(self.Model)
        res = await self.session.execute(stmt)
        await self.session.commit()
        return res.scalars().first()

    async def get_by_name(self, name: str) -> Model:
        stmt = select(self.Model).where(and_(self.Model.name == name))
        res = await self.session.execute(stmt)
        return res.scalars().first()

    async def get_one(self, read_id: int) -> Model:
        stmt = select(self.Model).where(and_(self.Model.id == read_id))
        res = await self.session.execute(stmt)
        return res.scalars().first()

    async def get(self, item_start: int, item_end: int) -> Sequence[Row]:
        stmt = (select(self.Model).
                order_by(self.Model.name).
                slice(item_start, item_end))
        res = await self.session.execute(stmt)
        return res.scalars().all()

    async def get_names_like(self, phrase: str, item_start: int, item_end: int) -> Sequence[Row]:
        stmt = (select(self.Model).
                where(self.Model.name.contains(phrase)).
                order_by(self.Model.name).
                slice(item_start, item_end))
        res = await self.session.execute(stmt)
        return res.scalars().all()

    async def update(self, update_id: int, **kw) -> Model:
        stmt = update(self.Model).where(and_(self.Model.id == update_id)).values(kw).returning(self.Model)
        res = await self.session.execute(stmt)
        await self.session.commit()
        return res.scalars().first()

    async def delete_data(self, delete_id: int) -> Model:
        stmt = delete(self.Model).where(and_(self.Model.id == delete_id)).returning(self.Model)
        res = await self.session.execute(stmt)
        await self.session.commit()
        return res.scalars().first()



class AbstractRepositoryLink(ABC):
    Model = None

    @abstractmethod
    async def get_link(self, left_id, right_id) -> Model:
        raise NotImplementedError

    @abstractmethod
    async def create_link(self, left_id: int, right_id: int) -> Model:
        raise NotImplementedError

    @abstractmethod
    async def delete_one_link(self, left_id: int, right_id: int) -> int():
        raise NotImplementedError

    @abstractmethod
    async def delete_all_left_links(self, left_id: int) -> int():
        raise NotImplementedError

    @abstractmethod
    async def delete_all_right_links(self, right_id: int) -> int():
        raise NotImplementedError

    @abstractmethod
    async def count_links_left(self, left_id) -> int():
        raise NotImplementedError

    @abstractmethod
    async def count_links_right(self, right_id) -> int():
        raise NotImplementedError


class RepositoryLink(AbstractRepositoryLink):
    Model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_link(self, left_id, right_id, aux: bool = None) -> Model:
        stmt = select(self.Model).where(
            and_(self.Model.left_id == left_id,
                 self.Model.right_id == right_id,
                 self.Model.returned == aux if aux is not None else True))
        res = await self.session.execute(stmt)
        return res.scalars().first()

    async def create_link(self, left_id, right_id) -> Model:
        stmt = (insert(self.Model).
                values({"left_id": left_id, "right_id": right_id}).
                on_conflict_do_nothing().
                returning(self.Model))
        res = await self.session.execute(stmt)
        await self.session.commit()
        return res.scalars().first()

    async def delete_one_link(self, left_id, right_id) -> int():
        stmt = delete(self.Model).where(
            and_(self.Model.left_id == left_id,
                 self.Model.right_id == right_id, ))
        res = await self.session.execute(stmt)
        await self.session.commit()
        return res.rowcount

    async def delete_all_left_links(self, left_id) -> int():
        stmt = delete(self.Model).where(and_(self.Model.left_id == left_id))
        res = await self.session.execute(stmt)
        await self.session.commit()
        return res.rowcount

    async def delete_all_right_links(self, right_id) -> int():
        stmt = delete(self.Model).where(and_(self.Model.right_id == right_id))
        res = await self.session.execute(stmt)
        await self.session.commit()
        return res.rowcount

    async def count_links_left(self, left_id) -> int():
        stmt = (select(func.count("*")).select_from(self.Model).
                where(and_(self.Model.left_id == left_id)))
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def count_links_right(self, right_id) -> int():
        stmt = (select(func.count("*")).select_from(self.Model).
                where(and_(self.Model.right_id == right_id)))
        res = await self.session.execute(stmt)
        return res.scalar_one()


