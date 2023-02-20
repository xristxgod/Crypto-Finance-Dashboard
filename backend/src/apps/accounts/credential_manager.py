import uuid
import json
from typing import NoReturn
from dataclasses import dataclass, asdict

import keyring

__all__ = (
    'BaseCredentialManager',
    'binance_manager',
    'Keys',
)


@dataclass()
class Keys:
    public: str
    secret: str


class BaseCredentialManager:
    service_name: str

    @classmethod
    def name(cls) -> str:
        return cls.__name__

    @classmethod
    def _encode(cls, keys: dict | Keys) -> str:
        if isinstance(keys, dict):
            value = json.dumps(dict(public=keys['public'], secret=keys['secret']))
        else:
            value = json.dumps(asdict(keys))
        return value.encode('utf-8').hex()

    @classmethod
    def _decode(cls, data: str) -> Keys:
        raw_keys = json.loads(bytes.fromhex(data).decode('utf-8'))
        return Keys(public=raw_keys['public'], secret=raw_keys['secret'])

    @classmethod
    async def set(cls, account_id: uuid.UUID, public: str, secret: str) -> NoReturn:
        if keyring.get_password(cls.service_name, str(account_id)) is None:
            keyring.set_password(cls.service_name, str(account_id), cls._encode(dict(public=public, secret=secret)))

    @classmethod
    async def get(cls, account_id: uuid.UUID) -> Keys:
        raw_data = keyring.get_password(cls.service_name, str(account_id))
        return cls._decode(raw_data)

    @classmethod
    async def remove(cls, account_id: uuid.UUID) -> NoReturn:
        if keyring.get_password(cls.service_name, str(account_id)) is not None:
            keyring.delete_password(cls.service_name, str(account_id))


class BinanceManager(BaseCredentialManager):
    service_name: str = 'binance'


binance_manager = BinanceManager
