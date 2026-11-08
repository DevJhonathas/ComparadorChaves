from pathlib import Path

from defusedxml import ElementTree as SafeET
from defusedxml.common import DefusedXmlException

from comparador.domain.entities.access_key import AccessKey


class XmlExtractionError(Exception):
    pass


class XmlKeyExtractor:
    ELEMENT_NAME = "infNFe"
    ID_ATTRIBUTE = "Id"
    ID_PREFIX = "NFe"

    def extract_from_file(self, file_path: str | Path) -> AccessKey:
        path = Path(file_path)

        try:
            root = SafeET.parse(path).getroot()
        except (OSError, SafeET.ParseError, DefusedXmlException) as exc:
            raise XmlExtractionError(
                f"Não foi possível ler o XML '{path.name}': {exc}"
            ) from exc

        info_elements = [
            element
            for element in root.iter()
            if self._local_name(element.tag) == self.ELEMENT_NAME
        ]

        if not info_elements:
            raise XmlExtractionError(
                f"O elemento '{self.ELEMENT_NAME}' não foi encontrado em '{path.name}'."
            )

        extracted_keys: set[str] = set()

        for element in info_elements:
            identifier = element.attrib.get(self.ID_ATTRIBUTE)

            if not identifier:
                raise XmlExtractionError(
                    f"O elemento '{self.ELEMENT_NAME}' não possui o atributo "
                    f"'{self.ID_ATTRIBUTE}' em '{path.name}'."
                )

            if not identifier.startswith(self.ID_PREFIX):
                raise XmlExtractionError(
                    f"O atributo '{self.ID_ATTRIBUTE}' de '{path.name}' deve começar "
                    f"exatamente com '{self.ID_PREFIX}'."
                )

            key_value = identifier[len(self.ID_PREFIX):]

            try:
                access_key = AccessKey(key_value)
            except (TypeError, ValueError) as exc:
                digits_count = len(key_value)
                raise XmlExtractionError(
                    f"Chave inválida no atributo '{self.ID_ATTRIBUTE}' de '{path.name}'. "
                    f"Foram encontrados {digits_count} caracteres após o prefixo "
                    f"'{self.ID_PREFIX}'; são esperados exatamente 44 dígitos."
                ) from exc

            extracted_keys.add(access_key.value)

        if len(extracted_keys) > 1:
            raise XmlExtractionError(
                f"O arquivo '{path.name}' contém mais de um elemento "
                f"'{self.ELEMENT_NAME}' com chaves diferentes. "
                "Esta versão espera uma NF-e por arquivo XML."
            )

        return AccessKey(extracted_keys.pop())

    @staticmethod
    def _local_name(tag: str) -> str:
        return tag.rsplit("}", 1)[-1]
