# tests/test_validate_service.py

import pytest
from freezegun import freeze_time
from unittest.mock import AsyncMock
from typing import Generator

from application.service.validate_service import ValidateService
from domain.user.exceptions import EmailAlreadyExists, UserNotFound
from domain.user.user_repo import IUserRepository
from domain.user.user import User
from sqlalchemy.ext.asyncio import AsyncSession


# ---------- Fixtures ----------


@pytest.fixture
def user_repo_mock(mocker) -> IUserRepository:
    repo = mocker.MagicMock(spec=IUserRepository)
    repo.get = AsyncMock()
    repo.get_by_email = AsyncMock()
    return repo


@pytest.fixture
def session_mock(mocker) -> AsyncSession:
    return mocker.MagicMock(spec=AsyncSession)


@pytest.fixture
def validate_service(user_repo_mock: IUserRepository) -> ValidateService:
    return ValidateService(user_repo=user_repo_mock)


@pytest.fixture
def dummy_user() -> User:
    return User.create(
        name="테스터",
        email="tester@example.com",
        password="hashed-password",
    )


# ---------- Test cases ----------

# --- user_validate_by_id ---


@freeze_time("2025-06-12")
@pytest.mark.asyncio
async def test_user_validate_by_id_success(
    validate_service, user_repo_mock, session_mock, dummy_user
):
    # -- 설정 --
    user_repo_mock.get.return_value = dummy_user

    # -- 실행 --
    user = await validate_service.user_validate_by_id(
        user_id=dummy_user.id,
        session=session_mock,
    )

    # -- 검증 --
    user_repo_mock.get.assert_awaited_once_with(
        id=dummy_user.id,
        session=session_mock,
    )
    assert user is dummy_user


@freeze_time("2025-06-12")
@pytest.mark.asyncio
async def test_user_validate_by_id_not_found(
    validate_service, user_repo_mock, session_mock
):
    # -- 설정 --
    user_repo_mock.get.return_value = None

    # -- 실행/검증 --
    with pytest.raises(UserNotFound):
        await validate_service.user_validate_by_id(
            user_id="not-found-id",
            session=session_mock,
        )

    user_repo_mock.get.assert_awaited_once_with(
        id="not-found-id",
        session=session_mock,
    )


# --- user_validate_by_email ---


@freeze_time("2025-06-12")
@pytest.mark.asyncio
async def test_user_validate_by_email_success(
    validate_service, user_repo_mock, session_mock, dummy_user
):
    # -- 설정 --
    user_repo_mock.get_by_email.return_value = dummy_user

    # -- 실행 --
    user = await validate_service.user_validate_by_email(
        email=dummy_user.profile.email,
        session=session_mock,
    )

    # -- 검증 --
    user_repo_mock.get_by_email.assert_awaited_once_with(
        email=dummy_user.profile.email,
        session=session_mock,
    )
    assert user is dummy_user


@freeze_time("2025-06-12")
@pytest.mark.asyncio
async def test_user_validate_by_email_not_found(
    validate_service, user_repo_mock, session_mock
):
    # -- 설정 --
    user_repo_mock.get_by_email.return_value = None

    # -- 실행/검증 --
    with pytest.raises(UserNotFound):
        await validate_service.user_validate_by_email(
            email="notfound@example.com",
            session=session_mock,
        )

    user_repo_mock.get_by_email.assert_awaited_once_with(
        email="notfound@example.com",
        session=session_mock,
    )


# --- email_duplicate_check ---


@freeze_time("2025-06-12")
@pytest.mark.asyncio
async def test_email_duplicate_check_no_duplicate(
    validate_service, user_repo_mock, session_mock
):
    # -- 설정 --
    user_repo_mock.get_by_email.return_value = None

    # -- 실행 --
    await validate_service.email_duplicate_check(
        email="unique@example.com",
        session=session_mock,
    )

    # -- 검증 --
    user_repo_mock.get_by_email.assert_awaited_once_with(
        email="unique@example.com",
        session=session_mock,
    )


@freeze_time("2025-06-12")
@pytest.mark.asyncio
async def test_email_duplicate_check_duplicated(
    validate_service, user_repo_mock, session_mock, dummy_user
):
    # -- 설정 --
    user_repo_mock.get_by_email.return_value = dummy_user

    # -- 실행/검증 --
    with pytest.raises(EmailAlreadyExists):
        await validate_service.email_duplicate_check(
            email=dummy_user.profile.email,
            session=session_mock,
        )

    user_repo_mock.get_by_email.assert_awaited_once_with(
        email=dummy_user.profile.email,
        session=session_mock,
    )
