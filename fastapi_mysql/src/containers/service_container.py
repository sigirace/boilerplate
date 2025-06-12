from dependency_injector import containers, providers
from application.service.validate_service import ValidateService
from containers.repository_container import RepositoryContainer


class ServiceContainer(containers.DeclarativeContainer):
    repository: RepositoryContainer = providers.DependenciesContainer()

    validate_service = providers.Factory(
        ValidateService,
        user_repo=repository.user_repository,
    )
