from PySide6.QtCore import QObject, Signal

from comparador.domain.entities.comparison_result import ComparisonResult
from comparador.domain.enums.comparison_status import ComparisonStatus
from comparador.infrastructure.xml.xml_directory_reader import XmlDirectoryReport


class ResultsViewModel(QObject):
    results_changed = Signal(object, str, object)

    def __init__(self) -> None:
        super().__init__()
        self.results: list[ComparisonResult] = []
        self.report: XmlDirectoryReport | None = None
        self.database_count = 0

    def set_results(
        self,
        results: list[ComparisonResult],
        report: XmlDirectoryReport,
        database_count: int,
    ) -> None:
        self.results = results
        self.report = report
        self.database_count = database_count
        found = sum(item.status == ComparisonStatus.FOUND for item in results)
        only_database = sum(item.status == ComparisonStatus.ONLY_DATABASE for item in results)
        only_xml = sum(item.status == ComparisonStatus.ONLY_XML for item in results)
        summary = (
            f"Banco: {database_count} ocorrência(s) | "
            f"XMLs: {report.total_files} arquivo(s) | "
            f"Encontradas: {found} | Somente banco: {only_database} | "
            f"Somente XML: {only_xml} | Erros XML: {len(report.errors)}"
        )
        self.results_changed.emit(results, summary, report.errors)
