import datetime

from sqlalchemy import Column
import sqlalchemy.types as fields
import sqlalchemy.schema as schema

from fastapi_users.db import SQLAlchemyBaseUserTable

from database import metadata


class Role(metadata):
    id = Column(fields.Integer, primary_key=True)
    name = Column(fields.String(length=255), nullable=False)
    permissions = Column(fields.JSON, default=dict)


class User(SQLAlchemyBaseUserTable[int], metadata):
    id = Column(fields.Integer, primary_key=True)
    username = Column(fields.String(length=255), nullable=False)
    email = Column(fields.String(length=255), nullable=False)
    registered_at = Column(fields.DateTime, default=datetime.datetime.now)
    role_id = Column(fields.Integer, schema.ForeignKey('role.id'))
    hashed_password = Column(fields.String(length=255), nullable=False)
    is_active = Column(fields.Boolean, default=True, nullable=False)
    is_superuser = Column(fields.Boolean, default=False, nullable=False)
    is_verified = Column(fields.Boolean, default=False, nullable=False)
