from dependency_injector import containers, providers
from containers.infra_container import InfraContainer
from containers.log_container import LogContainer
from containers.repository_container import RepositoryContainer
from containers.service_container import ServiceContainer
from containers.user_app_container import UserAppContainer
from containers.utils_container import UtilsContainer


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=[
            "interface.user.user_router",
            "middleware",
        ]
    )

    infra = providers.Container(InfraContainer)
    log = providers.Container(LogContainer, infra=infra)

    repository = providers.Container(RepositoryContainer)
    service = providers.Container(ServiceContainer, repository=repository)
    utils = providers.Container(UtilsContainer)

    user_app = providers.Container(
        UserAppContainer,
        repository=repository,
        service=service,
        utils=utils,
    )
