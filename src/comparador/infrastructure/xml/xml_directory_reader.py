from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from comparador.domain.entities.access_key import AccessKey
from comparador.infrastructure.xml.xml_key_extractor import XmlKeyExtractor, XmlExtractionError


@dataclass(frozen=True, slots=True)
class XmlFileError:
    file_path: Path
    message: str


@dataclass(frozen=True, slots=True)
class XmlDirectoryReport:
    entries: tuple[tuple[AccessKey, Path], ...]
    errors: tuple[XmlFileError, ...]
    total_files: int
    processed_files: int


ProgressCallback = Callable[[int, int, Path], None]


class XmlDirectoryReader:
    def __init__(self, extractor: XmlKeyExtractor) -> None:
        self._extractor = extractor

    def read_directory(
        self,
        directory: str | Path,
        recursive: bool = True,
        progress_callback: ProgressCallback | None = None,
    ) -> XmlDirectoryReport:
        root = Path(directory).expanduser()
        if not root.exists() or not root.is_dir():
            raise NotADirectoryError(f"A pasta informada não existe: {root}")

        iterator = root.rglob("*") if recursive else root.glob("*")
        files = sorted(
            (path for path in iterator if path.is_file() and path.suffix.casefold() == ".xml"),
            key=lambda path: str(path).casefold(),
        )

        entries: list[tuple[AccessKey, Path]] = []
        errors: list[XmlFileError] = []
        total = len(files)

        for index, file_path in enumerate(files, start=1):
            try:
                key = self._extractor.extract_from_file(file_path)
                entries.append((key, file_path))
            except XmlExtractionError as exc:
                errors.append(XmlFileError(file_path, str(exc)))
            except Exception as exc:
                errors.append(
                    XmlFileError(file_path, f"Erro inesperado ao processar arquivo: {exc}")
                )

            if progress_callback:
                progress_callback(index, total, file_path)

        return XmlDirectoryReport(
            entries=tuple(entries),
            errors=tuple(errors),
            total_files=total,
            processed_files=total,
        )
