from dependency_injector import containers, providers
from middleware.auth_middleware import AuthMiddleware
from containers.utils_container import UtilsContainer


class MiddlewareContainer(containers.DeclarativeContainer):
    utils: UtilsContainer = providers.DependenciesContainer()

    auth_middleware = providers.Factory(
        AuthMiddleware,
        jwt=utils.jwt,
    )
