from dataclasses import dataclass
from pathlib import Path

from comparador.domain.entities.access_key import AccessKey
from comparador.domain.enums.comparison_status import ComparisonStatus


@dataclass(frozen=True, slots=True)
class ComparisonResult:
    access_key: AccessKey
    status: ComparisonStatus
    database_occurrences: int
    xml_files: tuple[Path, ...]

    @property
    def xml_occurrences(self) -> int:
        return len(self.xml_files)

    @property
    def has_duplicates(self) -> bool:
        return self.database_occurrences > 1 or self.xml_occurrences > 1
