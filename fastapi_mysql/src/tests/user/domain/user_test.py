from datetime import datetime
from domain.user.user import User, Profile
from common.models import Lifecycle


def test_user_creation():
    user = User(
        id="TEST_ID",
        profile=Profile(
            name="TEST",
            email="TEST@EMAIL.COM",
        ),
        password="1234",
        lifecycle=Lifecycle(),
    )

    assert user.id == "TEST_ID"
    assert user.profile.name == "TEST"
    assert user.profile.email == "TEST@EMAIL.COM"
    assert user.password == "1234"
