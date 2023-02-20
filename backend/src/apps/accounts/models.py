from typing import Type, Optional, NoReturn

from tortoise import models
from tortoise import fields

from apps.common import mixins
from apps.common.models import AbstractUUIDIDModel
from apps.accounts.utils import keys_validator
from apps.accounts.credential_manager import BaseCredentialManager, Keys
from apps.accounts.validators import CredentialManagerValidator


class Service(models.Model):
    id = fields.CharField(pk=True, max_length=20)
    credential_manager_cls_name = fields.CharField(
        max_length=255,
        description='link to the object on the way: apps.accounts.credential_manager',
        validators=[CredentialManagerValidator()]
    )

    class CredentialManagerDoesNotExist(Exception):
        pass

    class Meta:
        table = "accounts_service"

    @property
    def name(self) -> str:
        return self.id

    @property
    def obj(self) -> Type[BaseCredentialManager]:
        credential_manager_module = __import__(
            'apps.accounts.credential_manager', locals=locals(), fromlist=[self.credential_manager_cls_name]
        )
        if hasattr(credential_manager_module, self.credential_manager_cls_name):
            return getattr(credential_manager_module, self.credential_manager_cls_name)
        raise self.CredentialManagerDoesNotExist()


class Account(mixins.TimestampMixin, AbstractUUIDIDModel):
    name = fields.CharField(max_length=255)
    service = fields.ForeignKeyField('default.Service', related_name='service_accounts',
                                     on_delete=fields.CASCADE)
    user = fields.ForeignKeyField('default.User', related_name='accounts',
                                  on_delete=fields.CASCADE)

    credential_manager: Type[BaseCredentialManager] = None

    class Meta:
        table = "accounts_account"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Add credential manager cls
        self.credential_manager = self.service.obj

    @keys_validator
    async def set_keys(self, public, secret) -> NoReturn:
        await self.credential_manager.set(self.id, public, secret)

    async def get_keys(self) -> Optional[Keys]:
        return await self.credential_manager.get(self.id)

    async def delete(self, using_db: Optional = None) -> NoReturn:
        await self.credential_manager.remove(self.id)
        await super().delete()
