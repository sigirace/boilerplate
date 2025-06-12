from unittest.mock import AsyncMock
import pytest
from typing import Tuple
from freezegun import freeze_time
from pytest_mock import MockerFixture

from application.user.create_user import CreateUser
from domain.user.user_repo import IUserRepository
from application.service.validate_service import ValidateService
from utils.crypto import Crypto
from domain.user.user import User  # User 도메인 모델
from sqlalchemy.ext.asyncio import AsyncSession


# ----------- Fixture ------------
@pytest.fixture
def service_dependencies(
    mocker: MockerFixture,
) -> Tuple[IUserRepository, ValidateService, Crypto, AsyncSession]:
    user_repo_mock = mocker.MagicMock(spec=IUserRepository)
    validate_service_mock = mocker.MagicMock(spec=ValidateService)
    crypto_mock = mocker.MagicMock(spec=Crypto)
    session_mock = AsyncMock(spec=AsyncSession)

    return (
        user_repo_mock,
        validate_service_mock,
        crypto_mock,
        session_mock,
    )


@pytest.mark.asyncio
@freeze_time("2025-06-12")
async def test_create_user_success(service_dependencies):
    (
        user_repo_mock,
        validate_service_mock,
        crypto_mock,
        session_mock,
    ) = service_dependencies

    # ---- 테스트 입력값 ----
    name = "test"
    email = "test@email.com"
    password = "1234"
    hashed_password = "hashed-1234"

    # ---- Mock 설정 ----
    crypto_mock.encrypt.return_value = hashed_password
    validate_service_mock.email_duplicate_check = AsyncMock()

    # User.create는 평문 password를 받으므로 실제 객체와 맞추기
    dummy_user = User.create(
        name=name,
        email=email,
        password=hashed_password,
    )

    user_repo_mock.save = AsyncMock(return_value=dummy_user)

    # ---- 유스케이스 인스턴스 ----
    create_user_service = CreateUser(
        user_repo=user_repo_mock,
        validate_service=validate_service_mock,
        crypt=crypto_mock,
    )

    # ---- 호출 ----
    user = await create_user_service(
        name=name,
        email=email,
        password=password,
        session=session_mock,
    )

    # ---- 검증 ----
    crypto_mock.encrypt.assert_called_once_with(password)
    validate_service_mock.email_duplicate_check.assert_awaited_once_with(
        email=email,
        session=session_mock,
    )
    user_repo_mock.save.assert_awaited_once_with(
        entity=user,
        session=session_mock,
    )

    assert user.profile.name == name
    assert user.profile.email == email
    assert user.password == hashed_password
