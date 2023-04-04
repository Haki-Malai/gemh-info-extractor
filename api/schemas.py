from marshmallow import Schema
from typing import Dict

from api.app import ma
from api.models import Company

paginated_schema_cache: Dict = {}


class StringPaginationSchema(ma.Schema):
    class Meta:
        ordered = True

    limit = ma.Integer()
    page = ma.Integer()
    count = ma.Integer(dump_only=True)
    total = ma.Integer(dump_only=True)


def paginated_collection(schema: Schema,
                         pagination_schema: Schema=StringPaginationSchema):
    """Create a paginated schema from a base schema
    :param schema: Base schema
    :param pagination_schema: Pagination schema
    :return: Paginated schema
    """
    if schema in paginated_schema_cache:
        return paginated_schema_cache[schema]

    class PaginatedSchema(ma.Schema):
        class Meta:
            ordered = True

        pagination = ma.Nested(pagination_schema)
        data = ma.Nested(schema, many=True)

    PaginatedSchema.__name__ = f'Paginated{schema.__class__.__name__}'
    paginated_schema_cache[schema] = PaginatedSchema
    return PaginatedSchema


class CompanySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Company
        load_instance = True
        include_fk = True
        ordered = True

    id = ma.auto_field()
    name = ma.auto_field()
    gemh = ma.auto_field()
    website = ma.auto_field()
    registration_date = ma.auto_field()