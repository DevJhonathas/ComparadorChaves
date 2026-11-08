from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFileDialog,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from comparador.domain.value_objects.database_config import DatabaseConfig


class SettingsView(QWidget):
    save_requested = Signal()
    test_requested = Signal()
    compare_requested = Signal()

    def __init__(self) -> None:
        super().__init__()
        self.driver = QComboBox()
        self.driver.setEditable(True)
        self.driver.addItems([
            "sqlite",
            "postgresql+psycopg",
            "mysql+pymysql",
            "mssql+pyodbc",
            "oracle+oracledb",
        ])
        self.database = QLineEdit()
        self.database.setPlaceholderText("Nome do banco ou caminho do arquivo SQLite")
        self.host = QLineEdit()
        self.host.setPlaceholderText("Ex.: localhost")
        self.port = QLineEdit()
        self.port.setPlaceholderText("Ex.: 5432")
        self.username = QLineEdit()
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        self.password.setPlaceholderText("Deixe vazio para usar senha salva")
        self.schema = QLineEdit()
        self.schema.setPlaceholderText("Opcional")
        self.odbc_driver = QLineEdit("ODBC Driver 18 for SQL Server")
        self.odbc_driver.setPlaceholderText("Ex.: ODBC Driver 18 for SQL Server")
        self.table = QLineEdit()
        self.column = QLineEdit()

        self.xml_directory = QLineEdit()
        self.xml_directory.setPlaceholderText("Selecione a pasta que contém os XMLs")
        browse_button = QPushButton("Procurar...")
        browse_button.clicked.connect(self._browse_directory)
        directory_row = QHBoxLayout()
        directory_row.addWidget(self.xml_directory, 1)
        directory_row.addWidget(browse_button)
        self.recursive = QCheckBox("Incluir subpastas")
        self.recursive.setChecked(True)

        database_group = QGroupBox("Conexão com o banco de dados")
        database_form = QFormLayout(database_group)
        database_form.addRow("Driver SQLAlchemy", self.driver)
        database_form.addRow("Banco de dados", self.database)
        database_form.addRow("Servidor / Host", self.host)
        database_form.addRow("Porta", self.port)
        database_form.addRow("Usuário", self.username)
        database_form.addRow("Senha", self.password)
        database_form.addRow("Schema", self.schema)
        database_form.addRow("Driver ODBC (SQL Server)", self.odbc_driver)
        database_form.addRow("Tabela", self.table)
        database_form.addRow("Coluna da chave", self.column)

        files_group = QGroupBox("Arquivos XML")
        files_form = QFormLayout(files_group)
        files_form.addRow("Pasta", directory_row)
        files_form.addRow("", self.recursive)

        self.save_button = QPushButton("Salvar configurações")
        self.test_button = QPushButton("Testar conexão")
        self.compare_button = QPushButton("Iniciar comparação")
        self.compare_button.setObjectName("primaryButton")

        actions = QHBoxLayout()
        actions.addWidget(self.save_button)
        actions.addStretch(1)
        actions.addWidget(self.test_button)
        actions.addWidget(self.compare_button)

        layout = QVBoxLayout(self)
        heading = QLabel("Configuração do comparador")
        heading.setObjectName("pageTitle")
        description = QLabel(
            "Informe os dados de acesso, a tabela que contém as chaves e a pasta dos XMLs."
        )
        description.setObjectName("mutedText")
        description.setWordWrap(True)
        layout.addWidget(heading)
        layout.addWidget(description)
        layout.addWidget(database_group)
        layout.addWidget(files_group)
        layout.addLayout(actions)
        layout.addStretch(1)

        self.save_button.clicked.connect(self.save_requested)
        self.test_button.clicked.connect(self.test_requested)
        self.compare_button.clicked.connect(self.compare_requested)

    def _browse_directory(self) -> None:
        directory = QFileDialog.getExistingDirectory(self, "Selecionar pasta de XMLs")
        if directory:
            self.xml_directory.setText(directory)

    def get_config(self) -> DatabaseConfig:
        port_text = self.port.text().strip()
        try:
            port = int(port_text) if port_text else None
        except ValueError as exc:
            raise ValueError("A porta deve ser um número inteiro.") from exc

        drivername = self.driver.currentText().strip()
        database = self.database.text().strip()
        host = self.host.text().strip()
        if drivername == "sqlite":
            host = ""
            port = None

        return DatabaseConfig(
            drivername=drivername,
            database=database,
            username=self.username.text().strip(),
            host=host,
            port=port,
            schema=self.schema.text().strip() or None,
            table=self.table.text().strip(),
            column=self.column.text().strip(),
            odbc_driver=self.odbc_driver.text().strip(),
        )

    def get_password(self) -> str:
        return self.password.text()

    def get_xml_directory(self) -> str:
        return self.xml_directory.text().strip()

    def get_recursive(self) -> bool:
        return self.recursive.isChecked()

    def set_values(self, values: dict) -> None:
        self.driver.setCurrentText(values.get("drivername", "sqlite"))
        self.database.setText(values.get("database", ""))
        self.host.setText(values.get("host", ""))
        self.port.setText(values.get("port", ""))
        self.username.setText(values.get("username", ""))
        self.schema.setText(values.get("schema", ""))
        self.odbc_driver.setText(
            values.get("odbc_driver", "ODBC Driver 18 for SQL Server")
        )
        self.table.setText(values.get("table", ""))
        self.column.setText(values.get("column", ""))
        self.xml_directory.setText(values.get("xml_directory", ""))
        self.recursive.setChecked(values.get("recursive", True))

    def set_busy(self, busy: bool) -> None:
        self.save_button.setEnabled(not busy)
        self.test_button.setEnabled(not busy)
        self.compare_button.setEnabled(not busy)
