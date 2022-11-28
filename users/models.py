from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String
from sqlalchemy.dialects.mysql import INTEGER


Base = declarative_base()
metadata = Base.metadata


class UserInfo(Base):

    __tablename__ = 'userinfo'

    id = Column(INTEGER(11), primary_key=True)
    username = Column(String(255))
    role = Column(String(50))
