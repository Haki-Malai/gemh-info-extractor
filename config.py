import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = None
    # MySQL
    MYSQL_SERVER = os.environ.get("MYSQL_SERVER")

    # Data pagination
    ITEMS_PER_BODY = 20
    # APIFairy
    APIFAIRY_TITLE = os.environ.get("APIFAIRY_TITLE")
    APIFAIRY_VERSION = os.environ.get("APIFAIRY_VERSION")
    APIFAIRY_UI = os.environ.get("APIFAIRY_UI")

    def __init__(self, username, password, database):
        self.SQLALCHEMY_DATABASE_URI = (
            f"mysql://{username}:{password}@"
            f"{self.MYSQL_SERVER}/{database}")


class DevelopmentConfig(Config):
    def __init__(self):
        super().__init__(
            os.environ.get("MYSQL_DEV_USERNAME"),
            os.environ.get("MYSQL_DEV_PASSWORD"),
            os.environ.get("MYSQL_DEV_DATABASE")
        )


class TestingConfig(Config):
    def __init__(self):
        super().__init__(
            os.environ.get("MYSQL_TEST_USERNAME"),
            os.environ.get("MYSQL_TEST_PASSWORD"),
            os.environ.get("MYSQL_TEST_DATABASE"))


class ProductionConfig(Config):
    def __init__(self):
        super().__init__(
            os.environ.get("MYSQL_PROD_USERNAME"),
            os.environ.get("MYSQL_PROD_PASSWORD"),
            os.environ.get("MYSQL_PROD_DATABASE"))


config = {
    'default': DevelopmentConfig(),
    'production': ProductionConfig(),
    'development': DevelopmentConfig(),
    'testing': TestingConfig()
}
