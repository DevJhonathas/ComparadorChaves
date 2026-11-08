import hashlib

import keyring

from comparador.domain.value_objects.database_config import DatabaseConfig


class CredentialStore:
    SERVICE_NAME = "comparador-chaves"

    @staticmethod
    def _credential_id(config: DatabaseConfig) -> str:
        identity = "|".join(
            [
                config.drivername,
                config.host,
                str(config.port or ""),
                config.database,
                config.username,
            ]
        )
        return hashlib.sha256(identity.encode("utf-8")).hexdigest()

    def save_password(self, config: DatabaseConfig, password: str) -> None:
        if password:
            keyring.set_password(self.SERVICE_NAME, self._credential_id(config), password)

    def get_password(self, config: DatabaseConfig) -> str | None:
        return keyring.get_password(self.SERVICE_NAME, self._credential_id(config))

    def delete_password(self, config: DatabaseConfig) -> None:
        try:
            keyring.delete_password(self.SERVICE_NAME, self._credential_id(config))
        except keyring.errors.PasswordDeleteError:
            pass
