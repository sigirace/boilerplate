from domain.user.user import UserList, Profile, User
from interface.user.user_dto import CreateUserRequest, UserListResponse, UserResponse


class UserInterfaceMapper:

    @staticmethod
    def to_domain(request: CreateUserRequest) -> User:
        return User(
            profile=Profile(
                name=request.name,
                email=request.email,
            ),
            password=request.password,
        )

    @staticmethod
    def to_response(user: User) -> UserResponse:
        return UserResponse(
            id=user.id,
            email=user.profile.email,
            name=user.profile.name,
        )

    @staticmethod
    def to_list_response(user_list: UserList) -> UserListResponse:
        return UserListResponse(
            page=user_list.page,
            total_count=user_list.total_count,
            users=[
                UserResponse(
                    id=user.id,
                    email=user.profile.email,
                    name=user.profile.name,
                )
                for user in user_list.users
            ],
        )
