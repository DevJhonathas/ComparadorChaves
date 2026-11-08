from comparador.domain.value_objects.database_config import DatabaseConfig
from comparador.infrastructure.database.connection_factory import ConnectionFactory


class ConnectionService:
    def __init__(self, connection_factory: ConnectionFactory) -> None:
        self._connection_factory = connection_factory

    def test_connection(self, config: DatabaseConfig, password: str | None = None) -> None:
        engine = self._connection_factory.create_engine(config, password)
        try:
            with engine.connect() as connection:
                validation_query = (
                    "SELECT 1 FROM DUAL"
                    if config.drivername.startswith("oracle+")
                    else "SELECT 1"
                )
                connection.exec_driver_sql(validation_query)
        finally:
            engine.dispose()
