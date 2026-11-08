from typing import Protocol, Any

from comparador.domain.value_objects.database_config import DatabaseConfig


class AccessKeyRepository(Protocol):
    def fetch_keys(self, connection: Any, config: DatabaseConfig) -> list[str]:
        ...
