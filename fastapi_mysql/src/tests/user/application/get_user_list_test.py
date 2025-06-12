# tests/application/user/test_get_list_users.py

import pytest
from unittest.mock import AsyncMock
from pytest_mock import MockerFixture
from sqlalchemy.ext.asyncio import AsyncSession

from application.user.get_list_users import GetListUsers
from domain.user.user_repo import IUserRepository
from domain.user.user import User, UserList


# ---------- Fixtures ----------


@pytest.fixture
def user_repo_mock(mocker: MockerFixture) -> IUserRepository:
    repo = mocker.MagicMock(spec=IUserRepository)
    repo.list = AsyncMock()
    return repo


@pytest.fixture
def session_mock(mocker: MockerFixture) -> AsyncSession:
    return mocker.MagicMock(spec=AsyncSession)


@pytest.fixture
def dummy_users() -> list[User]:
    return [
        User.create(name="홍길동", email="hong@example.com", password="pw1"),
        User.create(name="김철수", email="kim@example.com", password="pw2"),
    ]


# ---------- Test case ----------


@pytest.mark.asyncio
async def test_get_list_users_success(user_repo_mock, session_mock, dummy_users):
    # -- Arrange --
    total_count = 2
    page = 1
    item_per_page = 10

    user_repo_mock.list.return_value = (total_count, dummy_users)

    get_list_users_service = GetListUsers(user_repo=user_repo_mock)

    # -- Act --
    result: UserList = await get_list_users_service(
        page=page,
        item_per_page=item_per_page,
        session=session_mock,
    )

    # -- Assert --
    user_repo_mock.list.assert_awaited_once_with(
        page=page,
        item_per_page=item_per_page,
        session=session_mock,
    )

    assert isinstance(result, UserList)
    assert result.total_count == total_count
    assert result.page == page
    assert result.users == dummy_users
