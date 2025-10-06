import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-change-in-production'
    # Формат подключения: postgresql://username:password@localhost/database_name
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://timetable_db:erfjui@localhost/timetable'
    SQLALCHEMY_TRACK_MODIFICATIONS = False