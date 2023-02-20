from typing import Any

from tortoise import models
from fastapi.params import Query

from .patterns import Singleton


class BaseChoices(Singleton):
    """Loads values for choices from the database"""

    model: models.MODEL         # Model from which the data will be taken
    field_name: str = 'name'    # Field that will be output in `choices`

    __slots__ = (
        'default',
        'choices',
    )

    def __init__(self):
        self.default: Any = None
        self.choices: list[Any] = []

    async def setup(self):
        values: list[tuple] = await self.model.all().values_list(self.field_name)
        self.default = values.pop()[0]
        self.choices.append(self.default)
        for value in values:
            self.choices.append(value)

    def render(self) -> Query:
        return Query(default=self.default, enum=self.choices)
