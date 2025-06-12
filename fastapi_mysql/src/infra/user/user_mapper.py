from domain.user.user import User as UserVO
from infra.user.user import User


class UserInfraMapper:

    @staticmethod
    def to_orm_model(vo: UserVO) -> User:
        return User(
            id=vo.id,
            name=vo.profile.name,
            email=vo.profile.email,
            password=vo.password,
            created_at=vo.lifecycle.created_at,
            updated_at=vo.lifecycle.updated_at,
        )

    @staticmethod
    def to_vo(orm: User) -> UserVO:

        from domain.user.user import Profile, Lifecycle, User as UserVO

        return UserVO(
            id=orm.id,
            profile=Profile(
                name=orm.name,
                email=orm.email,
            ),
            password=orm.password,
            lifecycle=Lifecycle(
                created_at=orm.created_at,
                updated_at=orm.updated_at,
            ),
        )
