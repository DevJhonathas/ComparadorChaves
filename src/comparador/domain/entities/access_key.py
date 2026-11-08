import re
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AccessKey:
    value: str

    PATTERN = re.compile(r"[0-9]{44}")

    def __post_init__(self) -> None:
        if not isinstance(self.value, str):
            raise TypeError("A chave de acesso deve ser uma string.")

        normalized_value = self.value.strip()
        if not self.PATTERN.fullmatch(normalized_value):
            raise ValueError(
                "A chave de acesso deve conter exatamente 44 dígitos numéricos."
            )

        object.__setattr__(self, "value", normalized_value)
