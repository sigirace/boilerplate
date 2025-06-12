from dependency_injector import containers, providers
from application.user.create_user import CreateUser
from containers.repository_container import RepositoryContainer
from containers.utils_container import UtilsContainer
from containers.service_container import ServiceContainer
from application.user.get_list_users import GetListUsers
from application.user.delete_user import DeleteUser
from application.user.login import Login


class UserAppContainer(containers.DeclarativeContainer):
    repository: RepositoryContainer = providers.DependenciesContainer()
    service: ServiceContainer = providers.DependenciesContainer()
    utils: UtilsContainer = providers.DependenciesContainer()

    create_user = providers.Factory(
        CreateUser,
        user_repo=repository.user_repository,
        validate_service=service.validate_service,
        crypt=utils.crypt,
    )

    get_list_users = providers.Factory(
        GetListUsers,
        user_repo=repository.user_repository,
    )

    delete_user = providers.Factory(
        DeleteUser,
        user_repo=repository.user_repository,
        validate_service=service.validate_service,
    )

    login = providers.Factory(
        Login,
        validate_service=service.validate_service,
        crypt=utils.crypt,
        jwt=utils.jwt,
    )
