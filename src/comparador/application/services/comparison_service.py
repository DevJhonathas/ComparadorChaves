from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable

from comparador.domain.entities.access_key import AccessKey
from comparador.domain.entities.comparison_result import ComparisonResult
from comparador.domain.enums.comparison_status import ComparisonStatus


KeyInput = AccessKey | str
XmlKeyInput = tuple[KeyInput, str | Path]


class ComparisonService:
    def compare(
        self,
        database_keys: Iterable[KeyInput],
        xml_entries: Iterable[XmlKeyInput],
    ) -> list[ComparisonResult]:
        database_counts = Counter(self._normalize_key(key) for key in database_keys)
        xml_files: dict[AccessKey, list[Path]] = defaultdict(list)

        for key, file_path in xml_entries:
            normalized_key = self._normalize_key(key)
            xml_files[normalized_key].append(Path(file_path))

        all_keys = set(database_counts) | set(xml_files)
        results: list[ComparisonResult] = []

        for key in sorted(all_keys, key=lambda item: item.value):
            database_occurrences = database_counts.get(key, 0)
            files = tuple(
                sorted(xml_files.get(key, []), key=lambda path: str(path).casefold())
            )

            if database_occurrences and files:
                status = ComparisonStatus.FOUND
            elif database_occurrences:
                status = ComparisonStatus.ONLY_DATABASE
            else:
                status = ComparisonStatus.ONLY_XML

            results.append(
                ComparisonResult(
                    access_key=key,
                    status=status,
                    database_occurrences=database_occurrences,
                    xml_files=files,
                )
            )

        return results

    @staticmethod
    def _normalize_key(key: KeyInput) -> AccessKey:
        if isinstance(key, AccessKey):
            return key
        return AccessKey(key)
