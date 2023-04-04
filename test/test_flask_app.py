import pytest
from datetime import datetime
from flask import Flask, url_for
from typing import Generator

from api.app import create_app, redis_client
from api.models import Company
from api.schemas import CompanySchema

COMPANY_ROUTE: str = 'company.get_company'
COMPANIES_ROUTE: str = 'company.get_companies'


@pytest.fixture
def app() -> Generator[Flask, None, None]:
    """Create and configure a new app instance for each test.
    """
    app = create_app('testing')
    redis_client.flushall()
    with app.app_context():
        yield app
        redis_client.flushall()


@pytest.fixture
def client(app) -> Generator[Flask, None, None]:
    """A test client for the app.
    """
    return app.test_client()


@pytest.fixture
def db(app) -> Generator[Flask, None, None]:
    """Create a new database for a test.
    """
    with app.app_context():
        db = app.extensions['sqlalchemy'].db
        db.drop_all()
        db.create_all()
        yield db


@pytest.fixture
def companies(db) -> list:
    """Create some companies for a test.
    :param db: The db object.
    :return: A list of companies.
    """
    companies = [
        Company(name='Company A',
                website='www.company-a.com',
                gemh='111111111',
                registration_date=datetime(2001, 1, 1)),
        Company(name='Company B',
                website='www.company-b.com',
                gemh='222222222',
                registration_date=datetime(2002, 2, 2))]

    db.session.add_all(companies)
    db.session.commit()

    return companies


def test_index_redirects_to_api_docs(client) -> None:
    """Test that the index page redirects to the API docs.
    """
    response = client.get('/')
    assert response.status_code == 302
    assert response.headers['Location'] == url_for('apifairy.docs',
                                                   _external=False)


def test_get_companies(client, companies: list) -> None:
    """Test that the GET /companies endpoint returns all companies.
    """
    response = client.get(url_for(COMPANIES_ROUTE))
    assert response.status_code == 200

    data = response.get_json()['data']
    assert len(data) == len(companies)

    # Convert actual data to list of dictionaries
    actual_data = [dict(company) for company in data]

    # Ignore the 'id' field when comparing actual and expected data
    company_schema_dump = CompanySchema(many=True).dump(companies)
    for actual, expected in zip(actual_data, company_schema_dump):
        actual.pop('id')
        expected.pop('id')
        assert actual == expected


def test_get_company(client, companies: list) -> None:
    """Test that the GET /companies/<id> endpoint returns a company.
    """
    company_id = companies[0].id
    response = client.get(url_for(COMPANY_ROUTE, id=company_id))
    assert response.status_code == 200

    data = response.get_json()
    expected_data = CompanySchema().dump(companies[0])
    assert data == expected_data


def test_get_company_not_found(client) -> None:
    """Test that the GET /companies/<id> endpoint returns 404 when
    the company does not exist.
    """
    response = client.get(url_for(COMPANY_ROUTE, id=999))
    assert response.status_code == 404

    data = response.get_json()
    assert data['message'] == 'Not Found'


def test_get_companies_pagination(client, companies: list) -> None:
    """Test that the GET /companies endpoint returns the correct
    companies when using pagination.
    """
    response = client.get(url_for(COMPANIES_ROUTE, page=1, limit=1))
    assert response.status_code == 200

    data = response.get_json()['data']
    assert len(data) == 1

    # Convert actual data to list of dictionaries
    actual_data = [dict(company) for company in data]

    # Ignore the 'id' field when comparing actual and expected data
    company_schema_dump = CompanySchema(many=True).dump([companies[0]])
    for actual, expected in zip(actual_data, company_schema_dump):
        actual.pop('id')
        expected.pop('id')
        assert actual == expected

    response = client.get(url_for(COMPANIES_ROUTE, page=2, limit=1))
    assert response.status_code == 200

    data = response.get_json()['data']
    assert len(data) == 1

    # Convert actual data to list of dictionaries
    actual_data = [dict(company) for company in data]

    # Ignore the 'id' field when comparing actual and expected data
    company_schema_dump = CompanySchema(many=True).dump([companies[1]])
    for actual, expected in zip(actual_data, company_schema_dump):
        actual.pop('id')
        expected.pop('id')
        assert actual == expected

    response = client.get(url_for(COMPANIES_ROUTE, page=3, limit=1))
    assert response.status_code == 200

    data = response.get_json()['data']
    assert len(data) == 0
