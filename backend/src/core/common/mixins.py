from tortoise import fields


class CreatedMixin:
    created_at = fields.DatetimeField(null=True, auto_now_add=True)


class ModifiedMixin:
    modified_at = fields.DatetimeField(null=True, auto_now=True)


class TimestampMixin(CreatedMixin, ModifiedMixin):
    pass
