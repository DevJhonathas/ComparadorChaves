from pathlib import Path

import pytest

from comparador.infrastructure.xml.xml_key_extractor import XmlExtractionError, XmlKeyExtractor
from comparador.infrastructure.xml.xml_directory_reader import XmlDirectoryReader


FIXTURES = Path(__file__).parents[1] / "fixtures"
EXPECTED_KEY = "35261112345678000123550010000000011000000010"


def test_extract_key_from_inf_nfe_id():
    key = XmlKeyExtractor().extract_from_file(FIXTURES / "nfe_example.xml")
    assert key.value == EXPECTED_KEY


def test_extractor_uses_inf_nfe_id_not_ch_nfe(tmp_path):
    xml = f'''<?xml version="1.0" encoding="UTF-8"?>
    <NFe xmlns="http://www.portalfiscal.inf.br/nfe">
      <infNFe Id="NFe{EXPECTED_KEY}"><ide /></infNFe>
      <protNFe><infProt><chNFe>{'9' * 44}</chNFe></infProt></protNFe>
    </NFe>'''
    path = tmp_path / "nota.xml"
    path.write_text(xml, encoding="utf-8")

    assert XmlKeyExtractor().extract_from_file(path).value == EXPECTED_KEY


def test_missing_inf_nfe_raises_error():
    with pytest.raises(XmlExtractionError, match="infNFe"):
        XmlKeyExtractor().extract_from_file(FIXTURES / "missing_key.xml")


def test_missing_id_attribute_raises_error(tmp_path):
    path = tmp_path / "missing_id.xml"
    path.write_text(
        '<NFe xmlns="http://www.portalfiscal.inf.br/nfe"><infNFe /></NFe>',
        encoding="utf-8",
    )

    with pytest.raises(XmlExtractionError, match="não possui o atributo 'Id'"):
        XmlKeyExtractor().extract_from_file(path)


def test_wrong_prefix_raises_error(tmp_path):
    path = tmp_path / "wrong_prefix.xml"
    path.write_text(
        f'<NFe><infNFe Id="NFE{EXPECTED_KEY}" /></NFe>',
        encoding="utf-8",
    )

    with pytest.raises(XmlExtractionError, match="começar exatamente com 'NFe'"):
        XmlKeyExtractor().extract_from_file(path)


def test_id_with_48_digits_is_rejected_not_truncated(tmp_path):
    path = tmp_path / "48_digits.xml"
    path.write_text(
        f'<NFe><infNFe Id="NFe{"1" * 48}" /></NFe>',
        encoding="utf-8",
    )

    with pytest.raises(XmlExtractionError, match="48 caracteres.*44 dígitos"):
        XmlKeyExtractor().extract_from_file(path)


def test_invalid_xml_raises_error():
    with pytest.raises(XmlExtractionError, match="Não foi possível ler"):
        XmlKeyExtractor().extract_from_file(FIXTURES / "invalid.xml")


def test_directory_reader_collects_keys_and_errors(tmp_path):
    valid_xml = (
        '<NFe xmlns="http://www.portalfiscal.inf.br/nfe">'
        f'<infNFe Id="NFe{EXPECTED_KEY}" /></NFe>'
    )
    (tmp_path / "valid.xml").write_text(valid_xml, encoding="utf-8")
    (tmp_path / "invalid.xml").write_text("<broken>", encoding="utf-8")

    report = XmlDirectoryReader(XmlKeyExtractor()).read_directory(tmp_path)

    assert report.total_files == 2
    assert len(report.entries) == 1
    assert report.entries[0][0].value == EXPECTED_KEY
    assert len(report.errors) == 1
