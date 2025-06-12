# containers/log_container.py
from dependency_injector import containers, providers
from logs.log_handler import MotorLogHandler
from logs.log_factory import configure_root_logger
from containers.infra_container import InfraContainer


class LogContainer(containers.DeclarativeContainer):
    """로깅 전용 DI 컨테이너"""

    infra: InfraContainer = providers.DependenciesContainer()

    motor_handler = providers.Singleton(MotorLogHandler, db=infra.motor_db)

    # Resource → Callable 로 교체, lifespan 안에서 한 번 호출
    root_logger = providers.Callable(configure_root_logger, handler=motor_handler)
