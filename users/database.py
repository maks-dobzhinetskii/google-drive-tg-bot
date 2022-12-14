import databases

from sqlalchemy import create_engine


SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:postgres@localhost:5432/google_drive_tg_bot_user'
database = databases.Database(SQLALCHEMY_DATABASE_URL)
engine = create_engine(SQLALCHEMY_DATABASE_URL)
