from comparador.domain.value_objects.database_config import DatabaseConfig
from comparador.infrastructure.database.connection_factory import ConnectionFactory


def test_build_postgresql_url():
    config = DatabaseConfig(
        drivername="postgresql+psycopg",
        database="fiscal",
        username="usuario",
        host="db.exemplo.local",
        port=5432,
        table="documentos",
        column="chave_acesso",
    )

    url = ConnectionFactory().build_url(config, "p@ss:/word")

    assert url.drivername == "postgresql+psycopg"
    assert url.username == "usuario"
    assert url.password == "p@ss:/word"
    assert url.host == "db.exemplo.local"
    assert url.port == 5432
    assert url.database == "fiscal"


def test_build_mysql_url():
    config = DatabaseConfig(
        drivername="mysql+pymysql",
        database="fiscal",
        username="usuario",
        host="localhost",
        port=3306,
        table="documentos",
        column="chave_acesso",
    )

    url = ConnectionFactory().build_url(config, "senha")

    assert url.drivername == "mysql+pymysql"
    assert url.port == 3306


def test_build_sql_server_url_includes_odbc_driver():
    config = DatabaseConfig(
        drivername="mssql+pyodbc",
        database="fiscal",
        username="usuario",
        host="sqlserver.local",
        port=1433,
        table="documentos",
        column="chave_acesso",
        odbc_driver="ODBC Driver 18 for SQL Server",
    )

    url = ConnectionFactory().build_url(config, "senha")

    assert url.drivername == "mssql+pyodbc"
    assert url.query["driver"] == "ODBC Driver 18 for SQL Server"


def test_build_oracle_url_uses_service_name_as_database():
    config = DatabaseConfig(
        drivername="oracle+oracledb",
        database="ORCLPDB1",
        username="usuario",
        host="oracle.local",
        port=1521,
        table="DOCUMENTOS",
        column="CHAVE_ACESSO",
    )

    url = ConnectionFactory().build_url(config, "senha")

    assert url.drivername == "oracle+oracledb"
    assert url.database == "ORCLPDB1"
