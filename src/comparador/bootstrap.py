from comparador.application.services.comparison_service import ComparisonService
from comparador.application.services.connection_service import ConnectionService
from comparador.infrastructure.config.settings_repository import SettingsRepository
from comparador.infrastructure.database.connection_factory import ConnectionFactory
from comparador.infrastructure.database.key_repository import KeyRepository
from comparador.infrastructure.security.credential_store import CredentialStore
from comparador.infrastructure.xml.xml_directory_reader import XmlDirectoryReader
from comparador.infrastructure.xml.xml_key_extractor import XmlKeyExtractor
from comparador.presentation.viewmodels.main_viewmodel import MainViewModel
from comparador.presentation.viewmodels.results_viewmodel import ResultsViewModel
from comparador.presentation.views.main_window import MainWindow


def create_main_window() -> MainWindow:
    connection_factory = ConnectionFactory()
    key_repository = KeyRepository()
    xml_reader = XmlDirectoryReader(XmlKeyExtractor())
    comparison_service = ComparisonService()
    connection_service = ConnectionService(connection_factory)
    settings_repository = SettingsRepository()
    credential_store = CredentialStore()

    main_viewmodel = MainViewModel(
        connection_factory=connection_factory,
        key_repository=key_repository,
        xml_reader=xml_reader,
        comparison_service=comparison_service,
        connection_service=connection_service,
        settings_repository=settings_repository,
        credential_store=credential_store,
    )
    results_viewmodel = ResultsViewModel()
    return MainWindow(main_viewmodel, results_viewmodel)
