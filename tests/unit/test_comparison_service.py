from pathlib import Path

import pytest

from comparador.application.services.comparison_service import ComparisonService
from comparador.domain.entities.access_key import AccessKey
from comparador.domain.enums.comparison_status import ComparisonStatus


KEY_1 = "35261112345678000123550010000000011000000010"
KEY_2 = "35261112345678000123550010000000011000000011"
KEY_3 = "35261112345678000123550010000000011000000012"
KEY_4 = "35261112345678000123550010000000011000000013"


def test_compare_access_keys():
    service = ComparisonService()
    database_keys = [KEY_1, KEY_2, KEY_3]
    xml_entries = [
        (KEY_1, Path("documento_01.xml")),
        (KEY_3, Path("documento_02.xml")),
        (KEY_4, Path("documento_03.xml")),
    ]

    results = service.compare(database_keys, xml_entries)
    results_by_key = {result.access_key.value: result for result in results}

    assert len(results) == 4
    assert results_by_key[KEY_1].status == ComparisonStatus.FOUND
    assert results_by_key[KEY_2].status == ComparisonStatus.ONLY_DATABASE
    assert results_by_key[KEY_3].status == ComparisonStatus.FOUND
    assert results_by_key[KEY_4].status == ComparisonStatus.ONLY_XML


def test_detect_duplicate_keys():
    service = ComparisonService()
    results = service.compare(
        [KEY_1, KEY_1],
        [(KEY_1, Path("a.xml")), (KEY_1, Path("b.xml"))],
    )

    assert len(results) == 1
    assert results[0].has_duplicates
    assert results[0].database_occurrences == 2
    assert results[0].xml_occurrences == 2


def test_access_key_requires_exactly_44_ascii_digits():
    with pytest.raises(ValueError, match="exatamente 44 dígitos"):
        AccessKey("1234567890")

    with pytest.raises(ValueError, match="exatamente 44 dígitos"):
        AccessKey("1" * 48)

    with pytest.raises(ValueError, match="exatamente 44 dígitos"):
        AccessKey("1" * 43 + "９")
