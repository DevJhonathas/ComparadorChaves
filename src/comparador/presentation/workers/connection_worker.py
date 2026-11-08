from PySide6.QtCore import QThread, Signal

from comparador.application.services.connection_service import ConnectionService
from comparador.domain.value_objects.database_config import DatabaseConfig


class ConnectionWorker(QThread):
    succeeded = Signal(str)
    failed = Signal(str)

    def __init__(
        self,
        service: ConnectionService,
        config: DatabaseConfig,
        password: str | None,
    ) -> None:
        super().__init__()
        self._service = service
        self._config = config
        self._password = password

    def run(self) -> None:
        try:
            self._service.test_connection(self._config, self._password)
            self.succeeded.emit("Conexão realizada com sucesso.")
        except Exception as exc:
            self.failed.emit(str(exc))
