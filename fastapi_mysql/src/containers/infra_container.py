# containers/infra_container.py
from dependency_injector import containers, providers
from database.mongo import get_async_mongo_client, get_async_mongo_database


class InfraContainer(containers.DeclarativeContainer):
    """DB · 외부 인프라 객체"""

    motor_client = providers.Singleton(get_async_mongo_client)
    motor_db = providers.Singleton(
        get_async_mongo_database,
        client=motor_client,
    )
