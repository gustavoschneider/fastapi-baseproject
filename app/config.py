from logging.config import dictConfig
from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = 'BaseProject'
    app_version: str = '0.0.1'
    app_secret: str = None
    database_url: str = None
    log_level: str = 'NOTSET'
    
    class Config:
        env_file = '.env'

def get_settings() -> Settings:
    return Settings()

class LogConfig(BaseSettings):
    """Logging configuration to be set for the server"""

    LOGGER_NAME: str = 'baseproject'
    LOG_FORMAT: str = '%(levelprefix)s | %(asctime)s | %(message)s'
    LOG_LEVEL: str = 'DEBUG'

    # Logging config
    version = 1
    disable_existing_loggers = False
    formatters = {
        'default': {
            '()': 'uvicorn.logging.DefaultFormatter',
            'fmt': LOG_FORMAT,
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    }
    handlers = {
        'default': {
            'formatter': 'default',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stderr',
        },
    }
    loggers = {
        'baseproject': {'handlers': ['default'], 'level': LOG_LEVEL},
    }

settings = get_settings()
CONNECT_ARGS = { 'check_same_thread': False } if settings.database_url.startswith('sqlite') else {}
dictConfig(LogConfig().dict())
