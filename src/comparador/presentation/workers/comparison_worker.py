import logging

from PySide6.QtCore import QThread, Signal

from comparador.application.services.comparison_service import ComparisonService
from comparador.domain.value_objects.database_config import DatabaseConfig
from comparador.infrastructure.database.connection_factory import ConnectionFactory
from comparador.infrastructure.database.key_repository import KeyRepository
from comparador.infrastructure.xml.xml_directory_reader import XmlDirectoryReader


class ComparisonWorker(QThread):
    progress = Signal(int, str)
    completed = Signal(object, object, int)
    failed = Signal(str)

    def __init__(
        self,
        connection_factory: ConnectionFactory,
        key_repository: KeyRepository,
        xml_reader: XmlDirectoryReader,
        comparison_service: ComparisonService,
        config: DatabaseConfig,
        password: str | None,
        xml_directory: str,
        recursive: bool,
    ) -> None:
        super().__init__()
        self._connection_factory = connection_factory
        self._key_repository = key_repository
        self._xml_reader = xml_reader
        self._comparison_service = comparison_service
        self._config = config
        self._password = password
        self._xml_directory = xml_directory
        self._recursive = recursive

    def run(self) -> None:
        engine = None
        try:
            self.progress.emit(2, "Conectando ao banco de dados...")
            engine = self._connection_factory.create_engine(self._config, self._password)

            with engine.connect() as connection:
                self.progress.emit(10, "Consultando as chaves do banco...")
                database_keys = self._key_repository.fetch_keys(connection, self._config)

            self.progress.emit(20, "Localizando arquivos XML...")

            def report_progress(processed: int, total: int, path) -> None:
                percentage = 20 if total == 0 else 20 + int((processed / total) * 65)
                self.progress.emit(
                    percentage,
                    f"Lendo XML {processed}/{total}: {path.name}",
                )

            report = self._xml_reader.read_directory(
                self._xml_directory,
                recursive=self._recursive,
                progress_callback=report_progress,
            )

            self.progress.emit(90, "Comparando as chaves...")
            results = self._comparison_service.compare(database_keys, report.entries)
            self.progress.emit(100, "Comparação concluída.")
            self.completed.emit(results, report, len(database_keys))
        except Exception as exc:
            logging.getLogger(__name__).exception("Falha durante a comparação.")
            self.failed.emit(str(exc))
        finally:
            if engine is not None:
                engine.dispose()
