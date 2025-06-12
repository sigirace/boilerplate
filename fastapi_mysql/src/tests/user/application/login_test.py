# tests/application/user/test_login.py

import pytest
from unittest.mock import AsyncMock
from pytest_mock import MockerFixture
from sqlalchemy.ext.asyncio import AsyncSession

from application.user.login import Login
from application.service.validate_service import ValidateService
from domain.user.exceptions import NotAuthorized
from domain.user.user import User
from utils.crypto import Crypto
from utils.jwt import JWT


# ---------- Fixtures ----------


@pytest.fixture
def service_dependencies(mocker: MockerFixture):
    validate_service_mock = mocker.MagicMock(spec=ValidateService)
    crypto_mock = mocker.MagicMock(spec=Crypto)
    jwt_mock = mocker.MagicMock(spec=JWT)
    session_mock = mocker.MagicMock(spec=AsyncSession)
    return validate_service_mock, crypto_mock, jwt_mock, session_mock


@pytest.fixture
def dummy_user():
    return User.create(
        name="테스터",
        email="tester@example.com",
        password="hashed-password",
    )


# ---------- Test cases ----------


@pytest.mark.asyncio
async def test_login_success(service_dependencies, dummy_user):
    # -- Arrange --
    validate_service, crypto, jwt, session = service_dependencies
    validate_service.user_validate_by_email = AsyncMock(return_value=dummy_user)
    crypto.verify.return_value = True
    jwt.create_access_token.return_value = "access-token"
    jwt.create_refresh_token.return_value = "refresh-token"

    login_service = Login(
        validate_service=validate_service,
        crypt=crypto,
        jwt=jwt,
    )

    # -- Act --
    access_token, refresh_token = await login_service(
        email=dummy_user.profile.email,
        password="1234",
        session=session,
    )

    # -- Assert --
    validate_service.user_validate_by_email.assert_awaited_once_with(
        email=dummy_user.profile.email,
        session=session,
    )
    crypto.verify.assert_called_once_with("1234", dummy_user.password)
    jwt.create_access_token.assert_called_once()
    jwt.create_refresh_token.assert_called_once()
    assert access_token == "access-token"
    assert refresh_token == "refresh-token"


@pytest.mark.asyncio
async def test_login_fail_invalid_password(service_dependencies, dummy_user):
    # -- Arrange --
    validate_service, crypto, jwt, session = service_dependencies
    validate_service.user_validate_by_email = AsyncMock(return_value=dummy_user)
    crypto.verify.return_value = False

    login_service = Login(
        validate_service=validate_service,
        crypt=crypto,
        jwt=jwt,
    )

    # -- Act & Assert --
    with pytest.raises(NotAuthorized):
        await login_service(
            email=dummy_user.profile.email,
            password="wrong-password",
            session=session,
        )

    validate_service.user_validate_by_email.assert_awaited_once_with(
        email=dummy_user.profile.email,
        session=session,
    )
    crypto.verify.assert_called_once_with("wrong-password", dummy_user.password)
    jwt.create_access_token.assert_not_called()
    jwt.create_refresh_token.assert_not_called()
