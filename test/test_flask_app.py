import pytest
from datetime import datetime
from flask import url_for

from api.app import create_app
from api.models import Company
from api.schemas import CompanySchema


@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        yield app


@pytest.fixture
def client(app):
    return app.test_client()


def test_index_redirects_to_api_docs(client):
    response = client.get('/')
    assert response.status_code == 302
    assert response.headers['Location'] == url_for('apifairy.docs',
                                                   _external=False)


@pytest.fixture
def db(app):
    with app.app_context():
        db = app.extensions['sqlalchemy'].db
        db.drop_all()
        db.create_all()
        yield db


@pytest.fixture
def companies(db):
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


def test_get_companies(client, companies: list):
    response = client.get(url_for('company.get_companies'))
    assert response.status_code == 200

    data = response.get_json()
    assert len(data) == len(companies)

    # Convert actual data to list of dictionaries
    actual_data = [dict(company) for company in data]

    # Ignore the 'id' field when comparing actual and expected data
    company_schema_dump = CompanySchema(many=True).dump(companies)
    for actual, expected in zip(actual_data, company_schema_dump):
        actual.pop('id')
        expected.pop('id')
        assert actual == expected


def test_get_company(client, companies: list):
    company_id = companies[0].id
    response = client.get(url_for('company.get_company', id=company_id))
    assert response.status_code == 200

    data = response.get_json()
    expected_data = CompanySchema().dump(companies[0])
    assert data == expected_data


def test_get_company_not_found(client):
    response = client.get(url_for('company.get_company', id=999))
    assert response.status_code == 404

    data = response.get_json()
    assert data['message'] == 'Not Found'
