from flask import Blueprint, abort
from apifairy import response, other_responses

from api.app import db
from api.models import Company
from api.schemas import CompanySchema
from api.pagination import paginated_response

bp = Blueprint('company', __name__)

company_schema = CompanySchema()
companies_schema = CompanySchema(many=True)


@bp.route('/company')
@paginated_response(companies_schema)
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
    return db.session.get(Company, id) or abort(404)
