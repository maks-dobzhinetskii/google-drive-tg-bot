from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.selectable import Select

from users.models import Message, UserInfo, Folder
from users.database import engine


Session = sessionmaker(bind=engine)
session = Session()


def get_query_by_media_group_id(media_group_id: int) -> Select:
    return select(Message).where(Message.media_group_id == media_group_id)


def create_user(username: str, message_id: int) -> None:
    session.add(UserInfo(
        username=username,
        message_id=message_id
    ))
    session.commit()


def create_message(media_group_id, file_name, folder_id):
    session.add(Message(
        media_group_id=media_group_id,
        file_name=file_name,
        folder_id=folder_id
    ))
    session.commit()


def create_folder(name_folder, id_drive_folder):
    session.add(Folder(
        name_folder=name_folder,
        id_drive_folder=id_drive_folder,
    ))
    session.commit()


if __name__ == '__main__':
    for el in session.scalars(get_query_by_media_group_id(69)):
        print(el.file_name)
    create_folder('test_folder3', 'drive_id3')
    create_message(101, 'ghj.txt', 3)
    create_user('kik', 1)
