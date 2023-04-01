from flask import Blueprint
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import HTTPException, InternalServerError

from api.app import apifairy

bp = Blueprint('error', __name__)


@bp.app_errorhandler(HTTPException)
def http_error(error: HTTPException) -> tuple:
    return {
        'code': error.code,
        'message': error.name,
        'description': error.description,
    }, error.code


@bp.app_errorhandler(SQLAlchemyError)
def sqlalchemy_error(error: SQLAlchemyError) -> tuple:
    return {
        'code': InternalServerError.code,
        'message': InternalServerError().name,
        'description': InternalServerError.description,
    }, 500


@apifairy.error_handler
def validation_error(code: int, messages: list[str]) -> tuple:
    return {
        'code': code,
        'message': 'Validation Error',
        'description': ('The server found one or more errors in the '
                        'information that you sent.'),
        'errors': messages,
    }, code
