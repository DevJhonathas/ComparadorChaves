from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QLabel,
    QMainWindow,
    QMessageBox,
    QProgressBar,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from comparador.presentation.viewmodels.main_viewmodel import MainViewModel
from comparador.presentation.viewmodels.results_viewmodel import ResultsViewModel
from comparador.presentation.views.results_view import ResultsView
from comparador.presentation.views.settings_view import SettingsView


class MainWindow(QMainWindow):
    def __init__(self, main_viewmodel: MainViewModel, results_viewmodel: ResultsViewModel) -> None:
        super().__init__()
        self._main_viewmodel = main_viewmodel
        self._results_viewmodel = results_viewmodel
        self.setWindowTitle("Comparador de Chaves")
        self.resize(1120, 760)
        self.setMinimumSize(850, 600)

        self.settings_view = SettingsView()
        self.results_view = ResultsView()
        self.tabs = QTabWidget()
        self.tabs.addTab(self.settings_view, "Configurações")
        self.tabs.addTab(self.results_view, "Resultados")

        self.status_label = QLabel("Pronto para iniciar.")
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)

        footer = QWidget()
        footer_layout = QVBoxLayout(footer)
        footer_layout.setContentsMargins(0, 8, 0, 0)
        footer_layout.addWidget(self.status_label)
        footer_layout.addWidget(self.progress_bar)

        central = QWidget()
        layout = QVBoxLayout(central)
        layout.addWidget(self.tabs, 1)
        layout.addWidget(footer)
        self.setCentralWidget(central)

        self.settings_view.save_requested.connect(self._save_settings)
        self.settings_view.test_requested.connect(self._test_connection)
        self.settings_view.compare_requested.connect(self._start_comparison)
        self._main_viewmodel.progress_changed.connect(self._update_progress)
        self._main_viewmodel.comparison_finished.connect(self._comparison_finished)
        self._results_viewmodel.results_changed.connect(self.results_view.set_results)
        self._main_viewmodel.error_occurred.connect(self._show_error)
        self._main_viewmodel.connection_succeeded.connect(self._connection_succeeded)
        self._main_viewmodel.busy_changed.connect(self.settings_view.set_busy)
        self._main_viewmodel.busy_changed.connect(self._set_busy)

        self.settings_view.set_values(self._main_viewmodel.load_settings())
        self._apply_style()

    def _save_settings(self) -> None:
        try:
            config = self.settings_view.get_config()
            self._main_viewmodel.save_settings(
                config,
                self.settings_view.get_password(),
                self.settings_view.get_xml_directory(),
                self.settings_view.get_recursive(),
            )
        except Exception as exc:
            self._show_error(str(exc))
            return
        QMessageBox.information(self, "Configurações", "Configurações salvas.")

    def _test_connection(self) -> None:
        try:
            config = self.settings_view.get_config()
            self._main_viewmodel.test_connection(config, self.settings_view.get_password())
            self.status_label.setText("Testando conexão...")
        except Exception as exc:
            self._show_error(str(exc))

    def _start_comparison(self) -> None:
        try:
            config = self.settings_view.get_config()
            directory = self.settings_view.get_xml_directory()
            if not directory:
                raise ValueError("Selecione a pasta que contém os arquivos XML.")
            self._main_viewmodel.save_settings(
                config,
                self.settings_view.get_password(),
                directory,
                self.settings_view.get_recursive(),
            )
            self._main_viewmodel.start_comparison(
                config,
                self.settings_view.get_password(),
                directory,
                self.settings_view.get_recursive(),
            )
            self.progress_bar.setValue(0)
            self.status_label.setText("Preparando comparação...")
            self.tabs.setCurrentWidget(self.results_view)
        except Exception as exc:
            self._show_error(str(exc))

    def _update_progress(self, percentage: int, message: str) -> None:
        self.progress_bar.setValue(percentage)
        self.status_label.setText(message)

    def _comparison_finished(self, results, report, database_count: int) -> None:
        self._results_viewmodel.set_results(results, report, database_count)
        if report.errors:
            QMessageBox.warning(
                self,
                "Comparação concluída com avisos",
                f"A comparação terminou, mas {len(report.errors)} arquivo(s) XML não puderam ser processados. Consulte a seção de erros abaixo da tabela.",
            )
        else:
            QMessageBox.information(self, "Comparação concluída", "A comparação foi concluída.")

    @staticmethod
    def _summary_text(results, report, database_count: int) -> str:
        from comparador.domain.enums.comparison_status import ComparisonStatus
        found = sum(item.status == ComparisonStatus.FOUND for item in results)
        only_db = sum(item.status == ComparisonStatus.ONLY_DATABASE for item in results)
        only_xml = sum(item.status == ComparisonStatus.ONLY_XML for item in results)
        return (
            f"Banco: {database_count} ocorrência(s) | XMLs: {report.total_files} arquivo(s) | "
            f"Encontradas: {found} | Somente banco: {only_db} | "
            f"Somente XML: {only_xml} | Erros XML: {len(report.errors)}"
        )

    def _connection_succeeded(self, message: str) -> None:
        self.status_label.setText(message)
        QMessageBox.information(self, "Conexão", message)

    def _show_error(self, message: str) -> None:
        self.status_label.setText("Ocorreu um erro.")
        QMessageBox.critical(self, "Erro", message)

    def _set_busy(self, busy: bool) -> None:
        if not busy:
            self.progress_bar.setValue(100 if self.status_label.text() == "Comparação concluída." else self.progress_bar.value())

    def _apply_style(self) -> None:
        self.setStyleSheet("""
            QMainWindow, QWidget { background: #11131b; color: #e8eaf2; font-size: 13px; }
            QGroupBox { border: 1px solid #303546; border-radius: 9px; margin-top: 12px; padding: 12px; font-weight: 600; }
            QGroupBox::title { subcontrol-origin: margin; left: 12px; padding: 0 5px; }
            QLineEdit, QComboBox { background: #1b1f2b; border: 1px solid #373e52; border-radius: 6px; padding: 8px; color: #f2f3f8; }
            QLineEdit:focus, QComboBox:focus { border: 1px solid #8b72f5; }
            QPushButton { background: #292e3d; border: 1px solid #3b4358; border-radius: 7px; padding: 9px 14px; }
            QPushButton:hover { background: #353c50; }
            QPushButton:disabled { color: #777d8c; }
            QPushButton#primaryButton { background: #7557df; border: 0; font-weight: 600; }
            QPushButton#primaryButton:hover { background: #856bea; }
            QTabWidget::pane { border: 1px solid #303546; border-radius: 8px; }
            QTabBar::tab { background: #1a1e29; padding: 10px 18px; margin-right: 4px; border-top-left-radius: 6px; border-top-right-radius: 6px; }
            QTabBar::tab:selected { background: #292e3d; color: #b9a9ff; }
            QTableView { background: #171b25; alternate-background-color: #1c2130; gridline-color: #303546; border: 1px solid #303546; selection-background-color: #483d78; }
            QHeaderView::section { background: #222838; padding: 8px; border: 0; border-right: 1px solid #303546; }
            QProgressBar { border: 1px solid #303546; border-radius: 5px; text-align: center; background: #1b1f2b; }
            QProgressBar::chunk { background: #7557df; border-radius: 4px; }
            QLabel#pageTitle { font-size: 22px; font-weight: 700; }
            QLabel#mutedText { color: #9ca3b5; }
            QCheckBox { spacing: 8px; }
        """)
