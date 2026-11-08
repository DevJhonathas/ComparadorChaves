import csv
from pathlib import Path

from PySide6.QtCore import QSortFilterProxyModel, Qt
from PySide6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QTableView,
    QLineEdit,
    QPlainTextEdit,
    QVBoxLayout,
    QWidget,
)

from comparador.domain.entities.comparison_result import ComparisonResult
from comparador.presentation.models.comparison_table_model import ComparisonTableModel


class ResultsView(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self._results: list[ComparisonResult] = []
        self.summary = QLabel("Nenhuma comparação executada.")
        self.summary.setObjectName("mutedText")
        self.search = QLineEdit()
        self.search.setPlaceholderText("Filtrar por chave, situação ou arquivo...")
        self.export_button = QPushButton("Exportar CSV")
        self.export_button.setEnabled(False)

        self.table = QTableView()
        self.errors_label = QLabel("Arquivos que não puderam ser processados")
        self.errors_label.setObjectName("mutedText")
        self.errors_text = QPlainTextEdit()
        self.errors_text.setReadOnly(True)
        self.errors_text.setMaximumHeight(150)
        self.errors_label.hide()
        self.errors_text.hide()
        self.model = ComparisonTableModel()
        self.proxy = QSortFilterProxyModel(self)
        self.proxy.setSourceModel(self.model)
        self.proxy.setSortRole(Qt.ItemDataRole.UserRole)
        self.proxy.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.proxy.setFilterKeyColumn(-1)
        self.table.setModel(self.proxy)
        self.table.setSortingEnabled(True)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableView.EditTrigger.NoEditTriggers)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setColumnWidth(0, 300)
        self.table.setColumnWidth(1, 170)
        self.table.setColumnWidth(2, 150)
        self.table.setColumnWidth(3, 100)

        top = QHBoxLayout()
        top.addWidget(self.search, 1)
        top.addWidget(self.export_button)
        layout = QVBoxLayout(self)
        layout.addWidget(self.summary)
        layout.addLayout(top)
        layout.addWidget(self.table, 1)
        layout.addWidget(self.errors_label)
        layout.addWidget(self.errors_text)

        self.search.textChanged.connect(self.proxy.setFilterFixedString)
        self.export_button.clicked.connect(self._export_csv)

    def set_results(self, results: list[ComparisonResult], summary: str, errors=()) -> None:
        self._results = results
        self.model.set_results(results)
        self.summary.setText(summary)
        self.export_button.setEnabled(bool(results))
        error_lines = [f"{item.file_path}: {item.message}" for item in errors]
        self.errors_text.setPlainText("\n".join(error_lines))
        self.errors_label.setVisible(bool(error_lines))
        self.errors_text.setVisible(bool(error_lines))

    def _export_csv(self) -> None:
        if not self._results:
            return
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Exportar resultados",
            "resultado_comparacao.csv",
            "CSV (*.csv)",
        )
        if not path:
            return

        try:
            with Path(path).open("w", newline="", encoding="utf-8-sig") as file:
                writer = csv.writer(file, delimiter=";")
                writer.writerow([
                    "Chave de acesso",
                    "Situação",
                    "Ocorrências no banco",
                    "Ocorrências XML",
                    "Arquivos XML",
                    "Duplicada",
                ])
                for result in self._results:
                    writer.writerow([
                        result.access_key.value,
                        result.status.value,
                        result.database_occurrences,
                        result.xml_occurrences,
                        " | ".join(str(item) for item in result.xml_files),
                        "Sim" if result.has_duplicates else "Não",
                    ])
        except OSError as exc:
            QMessageBox.critical(self, "Falha na exportação", str(exc))
            return

        QMessageBox.information(self, "Exportação concluída", "O CSV foi salvo com sucesso.")
