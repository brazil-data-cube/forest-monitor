import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
APPNAME = os.environ.get('CLIENT_AUDIENCE', '')

def get_settings(env):
    return CONFIG.get(env)


class Config():
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'SQLALCHEMY_DATABASE_URI',
        'postgresql+psycopg2://localhost/test')
    


class ProductionConfig(Config):
    """Production Mode"""
    DEBUG = False


class DevelopmentConfig(Config):
    """Development Mode"""
    DEVELOPMENT = True


class TestingConfig(Config):
    """Testing Mode (Continous Integration)"""
    TESTING = True
    DEBUG = True


CONFIG = {
    "DevelopmentConfig": DevelopmentConfig(),
    "ProductionConfig": ProductionConfig(),
    "TestingConfig": TestingConfig()
}
