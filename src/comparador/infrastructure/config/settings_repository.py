from PySide6.QtCore import QSettings

from comparador.domain.value_objects.database_config import DatabaseConfig


class SettingsRepository:
    def __init__(self) -> None:
        self._settings = QSettings("ComparadorChaves", "ComparadorDesktop")

    def save(
        self,
        config: DatabaseConfig,
        xml_directory: str,
        recursive: bool,
    ) -> None:
        self._settings.beginGroup("database")
        for key, value in {
            "drivername": config.drivername,
            "database": config.database,
            "username": config.username,
            "host": config.host,
            "port": config.port if config.port is not None else "",
            "schema": config.schema or "",
            "table": config.table,
            "column": config.column,
            "odbc_driver": config.odbc_driver,
        }.items():
            self._settings.setValue(key, value)
        self._settings.endGroup()

        self._settings.beginGroup("files")
        self._settings.setValue("xml_directory", xml_directory)
        self._settings.setValue("recursive", recursive)
        self._settings.endGroup()
        self._settings.sync()

    def load(self) -> dict:
        self._settings.beginGroup("database")
        database = {
            "drivername": self._settings.value("drivername", "sqlite", type=str),
            "database": self._settings.value("database", "", type=str),
            "username": self._settings.value("username", "", type=str),
            "host": self._settings.value("host", "", type=str),
            "port": self._settings.value("port", "", type=str),
            "schema": self._settings.value("schema", "", type=str),
            "table": self._settings.value("table", "", type=str),
            "column": self._settings.value("column", "", type=str),
            "odbc_driver": self._settings.value(
                "odbc_driver", "ODBC Driver 18 for SQL Server", type=str
            ),
        }
        self._settings.endGroup()

        self._settings.beginGroup("files")
        files = {
            "xml_directory": self._settings.value("xml_directory", "", type=str),
            "recursive": self._settings.value("recursive", True, type=bool),
        }
        self._settings.endGroup()
        return {**database, **files}
