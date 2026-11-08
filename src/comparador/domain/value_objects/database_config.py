from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DatabaseConfig:
    drivername: str
    database: str
    username: str = ""
    host: str = ""
    port: int | None = None
    schema: str | None = None
    table: str = ""
    column: str = ""
    odbc_driver: str = "ODBC Driver 18 for SQL Server"

    def __post_init__(self) -> None:
        if not self.drivername.strip():
            raise ValueError("Informe o driver SQLAlchemy.")
        if not self.database.strip():
            raise ValueError("Informe o nome do banco ou o caminho do arquivo SQLite.")
        if not self.table.strip():
            raise ValueError("Informe a tabela que contém as chaves.")
        if not self.column.strip():
            raise ValueError("Informe a coluna que contém as chaves.")
        if self.port is not None and not 1 <= self.port <= 65535:
            raise ValueError("A porta deve estar entre 1 e 65535.")
        if self.drivername == "mssql+pyodbc" and not self.odbc_driver.strip():
            raise ValueError("Informe o driver ODBC instalado para o SQL Server.")
