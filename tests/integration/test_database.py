from sqlalchemy import create_engine, text

from comparador.domain.value_objects.database_config import DatabaseConfig
from comparador.infrastructure.database.key_repository import KeyRepository


KEY_1 = "35261112345678000123550010000000011000000010"
KEY_2 = "35261112345678000123550010000000011000000011"


def test_key_repository_reads_selected_column(tmp_path):
    database_path = tmp_path / "test.db"
    engine = create_engine(f"sqlite:///{database_path}")
    try:
        with engine.begin() as connection:
            connection.execute(text("CREATE TABLE documents (access_key TEXT)"))
            connection.execute(
                text("INSERT INTO documents (access_key) VALUES (:key)"),
                [{"key": KEY_1}, {"key": KEY_2}, {"key": None}],
            )

        config = DatabaseConfig(
            drivername="sqlite",
            database=str(database_path),
            table="documents",
            column="access_key",
        )
        with engine.connect() as connection:
            keys = KeyRepository().fetch_keys(connection, config)

        assert keys == [KEY_1, KEY_2]
    finally:
        engine.dispose()


def test_key_repository_rejects_numeric_column(tmp_path):
    database_path = tmp_path / "numeric.db"
    engine = create_engine(f"sqlite:///{database_path}")
    try:
        with engine.begin() as connection:
            connection.execute(text("CREATE TABLE documents (access_key INTEGER)"))
            connection.execute(text("INSERT INTO documents VALUES (123)"))

        config = DatabaseConfig(
            drivername="sqlite",
            database=str(database_path),
            table="documents",
            column="access_key",
        )

        with engine.connect() as connection:
            try:
                KeyRepository().fetch_keys(connection, config)
            except ValueError as exc:
                assert "deve ser textual" in str(exc)
            else:
                raise AssertionError("A coluna numérica deveria ser rejeitada.")
    finally:
        engine.dispose()
