from enum import Enum


class ComparisonStatus(str, Enum):
    FOUND = "Encontrada"
    ONLY_DATABASE = "Somente no banco"
    ONLY_XML = "Somente nos XMLs"
