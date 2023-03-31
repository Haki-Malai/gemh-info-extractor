from api.app import ma
from api.models import Company


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