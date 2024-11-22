class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///mydb.db'
    SECRET_KEY = 'your_secret_key'

class DevConfig(Config):
    DEBUG = True
