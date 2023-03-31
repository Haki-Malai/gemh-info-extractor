from flask import Blueprint
from apifairy import response, other_responses

from api.models import Company
from api.schemas import CompanySchema

bp = Blueprint('company', __name__)

company_schema = CompanySchema()
companies_schema = CompanySchema(many=True)


@bp.route('/company')
@response(companies_schema)
def get_companies():
    """Get Companies
    """
    return Company.query


@bp.route('/company/<int:id>')
@response(company_schema)
@other_responses({404: 'Company not found'})
def get_company(id: int):
    """Get Company
    """
    return Company.query.filter_by(id=id).first_or_404()
