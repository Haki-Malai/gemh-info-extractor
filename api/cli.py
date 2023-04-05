import click
from flask import Blueprint
from sqlalchemy.exc import IntegrityError
from warnings import warn

from api.app import db
from api.models import Company
from data_extractor import FileProcessor

bp = Blueprint('script', __name__, cli_group=None)


@bp.cli.command('extract',
                help='Extract data from text files in the ./txt folder.')
@click.option('--folder', default='./txt',
              help='Path to the folder containing the txt files')
def extract(folder: str) -> None:
    """Extract data from text files in the ./txt folder and insert them to the
    database.
    :param folder: Path to the folder containing the txt files.
    """
    fp = FileProcessor(folder=folder)
    company_data = fp.process_files()

    added_companies = 0
    for data in company_data:
        company = Company(name=data['name'],
                          gemh=data['gemh'],
                          website=data['website'],
                          registration_date=data['date'])
        db.session.add(company)
        try:
            db.session.commit()
            added_companies += 1
        except IntegrityError as e:
            db.session.rollback()
            print(f'Duplicate entry for {data["name"]}')
            warn(e)
    print(f'Successfully added {added_companies} companies to the database.')


@bp.cli.command('test', help='Run tests.')
@click.option('--coverage', is_flag=True, help='Run tests with coverage.')
def test(coverage: bool) -> None:
    """Run tests.
    :param coverage: Run tests with coverage.
    """
    import pytest

    if coverage:
        pytest.main(['--cov=api', '--cov-report=html'])
    else:
        pytest.main()