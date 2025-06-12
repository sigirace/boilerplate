# tests/application/user/test_delete_user.py

import pytest
from unittest.mock import AsyncMock
from freezegun import freeze_time
from pytest_mock import MockerFixture

from application.user.delete_user import DeleteUser
from application.service.validate_service import ValidateService
from domain.user.user_repo import IUserRepository
from domain.user.user import User
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.fixture
def service_dependencies(mocker: MockerFixture):
    user_repo_mock = mocker.MagicMock(spec=IUserRepository)
    validate_service_mock = mocker.MagicMock(spec=ValidateService)
    session_mock = mocker.MagicMock(spec=AsyncSession)

    return user_repo_mock, validate_service_mock, session_mock


@pytest.fixture
def dummy_user() -> User:
    return User.create(
        name="삭제용유저",
        email="delete@example.com",
        password="secret",
    )


@freeze_time("2025-06-12")
@pytest.mark.asyncio
async def test_delete_user_success(service_dependencies, dummy_user):
    # -- Arrange --
    user_repo_mock, validate_service_mock, session_mock = service_dependencies

    validate_service_mock.user_validate_by_id = AsyncMock(return_value=dummy_user)
    user_repo_mock.delete = AsyncMock()

    delete_user_service = DeleteUser(
        user_repo=user_repo_mock,
        validate_service=validate_service_mock,
    )

    # -- Act --
    await delete_user_service(
        user_id=dummy_user.id,
        session=session_mock,
    )

    # -- Assert --
    validate_service_mock.user_validate_by_id.assert_awaited_once_with(
        user_id=dummy_user.id,
        session=session_mock,
    )

    user_repo_mock.delete.assert_awaited_once_with(
        id=dummy_user.id,
        session=session_mock,
    )
