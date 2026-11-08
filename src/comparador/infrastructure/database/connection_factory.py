from sqlalchemy import create_engine
from sqlalchemy.engine import Engine, URL

from comparador.domain.value_objects.database_config import DatabaseConfig


class ConnectionFactory:
    def build_url(
        self,
        config: DatabaseConfig,
        password: str | None = None,
    ) -> URL:
        query: dict[str, str] = {}

        if config.drivername == "mssql+pyodbc":
            query["driver"] = config.odbc_driver

        return URL.create(
            drivername=config.drivername,
            username=config.username or None,
            password=password or None,
            host=config.host or None,
            port=config.port,
            database=config.database,
            query=query,
        )

    def create_engine(
        self,
        config: DatabaseConfig,
        password: str | None = None,
    ) -> Engine:
        url = self.build_url(config, password)
        options = {"pool_pre_ping": True}

        if config.drivername == "sqlite":
            options["connect_args"] = {"timeout": 15}

        return create_engine(url, **options)
