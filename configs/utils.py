import os


def is_production_mode():
    return os.environ.get('PRODUCTION', 'false').lower() == 'true'
