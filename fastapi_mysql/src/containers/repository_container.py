from dependency_injector import containers, providers
from infra.user.user_repo_impl import UserRepositoryImpl


class RepositoryContainer(containers.DeclarativeContainer):

    user_repository = providers.Factory(UserRepositoryImpl)
