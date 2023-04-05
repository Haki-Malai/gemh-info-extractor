import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # Flask
    JSON_SORT_KEYS: bool = False

    # SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = True
    SQLALCHEMY_DATABASE_URI: str | None = None

    # MySQL
    MYSQL_SERVER: str = os.environ.get('MYSQL_SERVER')

    # Data pagination
    ITEMS_PER_BODY: int = 20

    # APIFairy
    APIFAIRY_TITLE: str = os.environ.get('APIFAIRY_TITLE')
    APIFAIRY_VERSION: str = os.environ.get('APIFAIRY_VERSION')
    APIFAIRY_UI: str = os.environ.get('APIFAIRY_UI')

    # Redis
    REDIS_HOST = os.environ.get('REDIS_HOST')
    CACHE_TIMEOUT: int = 60 * 60 * 24

    def __init__(self, username, password, database):
        self.SQLALCHEMY_DATABASE_URI = (
            f'mysql://{username}:{password}@'
            f'{self.MYSQL_SERVER}/{database}')


class DevelopmentConfig(Config):
    def __init__(self):
        super().__init__(
            os.environ.get('MYSQL_DEV_USERNAME'),
            os.environ.get('MYSQL_DEV_PASSWORD'),
            os.environ.get('MYSQL_DEV_DATABASE')
        )


class TestingConfig(Config):
    # For validating API urls
    SERVER_NAME: str = '127.0.0.1:5000'
    
    def __init__(self):
        super().__init__(
            os.environ.get('MYSQL_TEST_USERNAME'),
            os.environ.get('MYSQL_TEST_PASSWORD'),
            os.environ.get('MYSQL_TEST_DATABASE'))


class ProductionConfig(Config):
    def __init__(self):
        super().__init__(
            os.environ.get('MYSQL_PROD_USERNAME'),
            os.environ.get('MYSQL_PROD_PASSWORD'),
            os.environ.get('MYSQL_PROD_DATABASE'))


config = {
    'default': DevelopmentConfig(),
    'production': ProductionConfig(),
    'development': DevelopmentConfig(),
    'testing': TestingConfig()
}
