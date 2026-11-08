from sqlalchemy import MetaData, Table, select
from sqlalchemy.engine import Connection

from comparador.domain.value_objects.database_config import DatabaseConfig


class KeyRepository:
    def fetch_keys(self, connection: Connection, config: DatabaseConfig) -> list[str]:
        metadata = MetaData()
        table = Table(
            config.table,
            metadata,
            schema=config.schema,
            autoload_with=connection,
        )

        if config.column not in table.c:
            available = ", ".join(table.c.keys())
            raise ValueError(
                f"A coluna '{config.column}' não existe na tabela '{config.table}'. "
                f"Colunas disponíveis: {available}"
            )

        statement = select(table.c[config.column])
        values: list[str] = []

        for value in connection.execute(statement).scalars():
            if value is None:
                continue

            if not isinstance(value, str):
                raise ValueError(
                    f"A coluna '{config.column}' deve ser textual (CHAR/VARCHAR/TEXT). "
                    "Não use um tipo numérico para armazenar chaves de acesso, pois "
                    "isso pode remover zeros à esquerda."
                )

            normalized = value.strip()
            if normalized:
                values.append(normalized)

        return values
