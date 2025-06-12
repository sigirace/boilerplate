from dependency_injector import containers, providers

from utils.jwt import JWT
from utils.crypto import Crypto


class UtilsContainer(containers.DeclarativeContainer):

    crypt = providers.Factory(Crypto)
    jwt = providers.Factory(JWT)
