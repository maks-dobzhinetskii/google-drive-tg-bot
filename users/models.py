from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.mysql import INTEGER


Base = declarative_base()
metadata = Base.metadata


class Folder(Base):
    __tablename__ = 'folder'

    id = Column(INTEGER(20), primary_key=True)
    name_folder = Column(String(255))
    id_drive_folder = Column(String(255))


class Message(Base):
    __tablename__ = 'message'

    id = Column(INTEGER(20), primary_key=True)
    media_group_id = Column(String(50))
    file_name = Column(String(50))
    folder_id = Column(INTEGER(10), ForeignKey('folder.id'))
    user_id = Column(INTEGER(10), ForeignKey('userinfo.id'))


class UserInfo(Base):
    __tablename__ = 'userinfo'

    id = Column(INTEGER(20), primary_key=True)
    username = Column(String(255))
