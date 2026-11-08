from PySide6.QtCore import QObject, Signal

from comparador.application.services.comparison_service import ComparisonService
from comparador.application.services.connection_service import ConnectionService
from comparador.domain.value_objects.database_config import DatabaseConfig
from comparador.infrastructure.config.settings_repository import SettingsRepository
from comparador.infrastructure.database.connection_factory import ConnectionFactory
from comparador.infrastructure.database.key_repository import KeyRepository
from comparador.infrastructure.security.credential_store import CredentialStore
from comparador.infrastructure.xml.xml_directory_reader import XmlDirectoryReader
from comparador.presentation.workers.comparison_worker import ComparisonWorker
from comparador.presentation.workers.connection_worker import ConnectionWorker


class MainViewModel(QObject):
    progress_changed = Signal(int, str)
    comparison_finished = Signal(object, object, int)
    error_occurred = Signal(str)
    connection_succeeded = Signal(str)
    busy_changed = Signal(bool)

    def __init__(
        self,
        connection_factory: ConnectionFactory,
        key_repository: KeyRepository,
        xml_reader: XmlDirectoryReader,
        comparison_service: ComparisonService,
        connection_service: ConnectionService,
        settings_repository: SettingsRepository,
        credential_store: CredentialStore,
    ) -> None:
        super().__init__()
        self._connection_factory = connection_factory
        self._key_repository = key_repository
        self._xml_reader = xml_reader
        self._comparison_service = comparison_service
        self._connection_service = connection_service
        self._settings_repository = settings_repository
        self._credential_store = credential_store
        self._comparison_worker: ComparisonWorker | None = None
        self._connection_worker: ConnectionWorker | None = None

    def load_settings(self) -> dict:
        return self._settings_repository.load()

    def save_settings(
        self,
        config: DatabaseConfig,
        password: str,
        xml_directory: str,
        recursive: bool,
    ) -> None:
        self._settings_repository.save(config, xml_directory, recursive)
        if password:
            try:
                self._credential_store.save_password(config, password)
            except Exception:
                import logging
                logging.getLogger(__name__).exception("Não foi possível salvar a credencial no cofre do sistema.")

    def test_connection(self, config: DatabaseConfig, password: str) -> None:
        if self._connection_worker and self._connection_worker.isRunning():
            return
        try:
            stored_password = password or self._credential_store.get_password(config)
        except Exception:
            stored_password = password or None
        self._connection_worker = ConnectionWorker(
            self._connection_service,
            config,
            stored_password,
        )
        self._connection_worker.succeeded.connect(self.connection_succeeded)
        self._connection_worker.failed.connect(self.error_occurred)
        self._connection_worker.finished.connect(lambda: self.busy_changed.emit(False))
        self.busy_changed.emit(True)
        self._connection_worker.start()

    def start_comparison(
        self,
        config: DatabaseConfig,
        password: str,
        xml_directory: str,
        recursive: bool,
    ) -> None:
        if self._comparison_worker and self._comparison_worker.isRunning():
            return
        try:
            stored_password = password or self._credential_store.get_password(config)
        except Exception:
            stored_password = password or None
        self._comparison_worker = ComparisonWorker(
            self._connection_factory,
            self._key_repository,
            self._xml_reader,
            self._comparison_service,
            config,
            stored_password,
            xml_directory,
            recursive,
        )
        self._comparison_worker.progress.connect(self.progress_changed)
        self._comparison_worker.completed.connect(self.comparison_finished)
        self._comparison_worker.failed.connect(self.error_occurred)
        self._comparison_worker.finished.connect(lambda: self.busy_changed.emit(False))
        self.busy_changed.emit(True)
        self._comparison_worker.start()
