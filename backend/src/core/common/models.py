from tortoise import models
from tortoise import fields


class AbstractModel(models.Model):
    id = fields.IntField(pk=True)

    class Meta:
        abstract = True