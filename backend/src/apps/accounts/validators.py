from typing import Type

from tortoise.validators import Validator, ValidationError

from .credential_manager import BaseCredentialManager
from apps.accounts import credential_manager as cm


class CredentialManagerValidator(Validator):
    credential_managers_cls: list[Type[BaseCredentialManager]] = (
        cm.BinanceManager,
    )

    def __call__(self, value: str):
        for manager in self.credential_managers_cls:
            if value == manager.name():
                return
        else:
            raise ValidationError(f'This repository `{value}` does not exist')
