from tortoise import models
from tortoise import fields


class AbstractIntIDModel(models.Model):
    id = fields.IntField(pk=True)

    class Meta:
        abstract = True

