from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt

from comparador.domain.entities.comparison_result import ComparisonResult


class ComparisonTableModel(QAbstractTableModel):
    HEADERS = ["Chave de acesso", "Situação", "Ocorrências no banco", "Arquivos XML", "Arquivos"]

    def __init__(self, results: list[ComparisonResult] | None = None) -> None:
        super().__init__()
        self._results = results or []

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return 0 if parent.isValid() else len(self._results)

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return 0 if parent.isValid() else len(self.HEADERS)

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole):
        if not index.isValid() or not (0 <= index.row() < len(self._results)):
            return None

        result = self._results[index.row()]
        files = [str(path) for path in result.xml_files]
        short_files = " | ".join(path.name for path in result.xml_files)
        status = result.status.value
        if result.has_duplicates:
            status += " (duplicada)"

        values = [
            result.access_key.value,
            status,
            result.database_occurrences,
            result.xml_occurrences,
            short_files,
        ]

        if role == Qt.ItemDataRole.DisplayRole:
            return values[index.column()]
        if role == Qt.ItemDataRole.UserRole:
            return [
                result.access_key.value,
                status,
                result.database_occurrences,
                result.xml_occurrences,
                short_files.casefold(),
            ][index.column()]
        if role == Qt.ItemDataRole.ToolTipRole and index.column() == 4:
            return "\n".join(files)
        if role == Qt.ItemDataRole.TextAlignmentRole and index.column() in (2, 3):
            return int(Qt.AlignmentFlag.AlignCenter)
        return None

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            if 0 <= section < len(self.HEADERS):
                return self.HEADERS[section]
        return None

    def set_results(self, results: list[ComparisonResult]) -> None:
        self.beginResetModel()
        self._results = results
        self.endResetModel()

    def result_at(self, row: int) -> ComparisonResult:
        return self._results[row]
