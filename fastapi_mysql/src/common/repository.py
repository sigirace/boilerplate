from abc import ABC, abstractmethod
from typing import Generic, Tuple, TypeVar, Optional, List
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T")


class BaseRepository(ABC, Generic[T]):
    @abstractmethod
    async def get(
        self,
        id: str,
        session: AsyncSession,
    ) -> Optional[T]:
        """ID로 조회"""
        raise NotImplementedError

    @abstractmethod
    async def list(
        self,
        page: int,
        item_per_page: int,
        session: AsyncSession,
    ) -> Tuple[int, List[T]]:
        """전체 리스트 조회"""
        raise NotImplementedError

    @abstractmethod
    async def save(
        self,
        entity: T,
        session: AsyncSession,
    ) -> None:
        """엔티티 저장 (insert or update)"""
        raise NotImplementedError

    # @abstractmethod
    # async def update(self, entity: T) -> None:
    #     """엔티티 업데이트"""
    #     raise NotImplementedError

    @abstractmethod
    async def delete(
        self,
        id: str,
        session: AsyncSession,
    ) -> None:
        """Id 기반 삭제"""
        raise NotImplementedError
