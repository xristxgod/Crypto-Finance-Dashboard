from apps.common.choices import BaseChoices
from .models import Service

__all__ = (
    'service_choices',
)


class ServiceChoices(BaseChoices):
    model = Service
    field_name = 'id'


service_choices = ServiceChoices()
