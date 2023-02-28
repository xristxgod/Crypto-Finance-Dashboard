from fastapi_users import schemas
from fastapi_users.models import ID

__all__ = (
    'BodySubModel',
)


class BodySubModel(schemas.CreateUpdateDictModel):
    user_id: ID
