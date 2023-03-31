import click
from flask import Blueprint

bp = Blueprint('script', __name__, cli_group=None)


@bp.cli.command('smth', help='smth')
def smth():
    pass