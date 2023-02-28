import uuid

from tortoise import models
from tortoise import fields


class AbstractIntIDModel(models.Model):
    id = fields.IntField(pk=True)

    class Meta:
        abstract = True


class AbstractUUIDIDModel(models.Model):
    id = fields.UUIDField(pk=True, default=uuid.uuid4)

    class Meta:
        abstract = True
