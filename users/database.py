import os

import databases
from sqlalchemy import create_engine

SQLALCHEMY_DATABASE_URL = os.getenv("DB_URL")
database = databases.Database(SQLALCHEMY_DATABASE_URL)
engine = create_engine(SQLALCHEMY_DATABASE_URL)
