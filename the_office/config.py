"""
config.py

Stores all configurations used by the application from database URLs to Secret keys to extension settings.
"""

import os

configs = {
    'development': 'the_office.config.DevelopmentConfig',
    'testing': 'the_office.config.TestingConfig',
    'production': 'the_office.config.ProductionConfig'
}


class Config:
    """
    Base configuration.
    """
    pass


class DevelopmentConfig(Config):
    """
    Insecure and unrecommended config for use during development.
    """
    SECRET_KEY = 'INSECURE'


class TestingConfig(DevelopmentConfig):
    """
    Configuration used for testing the application.
    """
    TESTING = True
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    """
    Configuration used for running in secure production environment.
    """
    SECRET_KEY = os.getenv('SECRET_KEY')
