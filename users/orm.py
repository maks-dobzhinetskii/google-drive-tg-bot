from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.selectable import Select

from users.models import Message, UserInfo, Folder
from users.database import engine


Session = sessionmaker(bind=engine)
session = Session()


def get_query_by_media_group_id(media_group_id: int) -> Select:
    return select(Message).where(Message.media_group_id == media_group_id)


def get_message_list_of_user(username: int) -> str:
    file_name, folder_id = (
        session.query(Message.file_name, Message.folder_id)
        .join(UserInfo, Message.user_id == UserInfo.id)
        .where(UserInfo.username == username)
        .group_by(Message.file_name, Message.folder_id)
    )
    return file_name, folder_id


def get_folder_info(folder_id: int) -> Select:
    folder_name, id_drive_folder = (
        session.query(Folder.name_folder, Folder.id_drive_folder)
        .join(Message, Folder.id == Message.folder_id)
        .where(Message.folder_id == folder_id)
        .group_by(Folder.id_drive_folder, Folder.name_folder)
        .first()
    )
    return folder_name, id_drive_folder


def get_folder_info_by_id_drive_folder(id_drive_folder: str) -> Select:
    return session.query(Folder).where(Folder.id_drive_folder == id_drive_folder)


def create_user(username: str) -> UserInfo:
    user = UserInfo(username=username)
    session.add(user)
    session.commit()
    return user


def create_message(media_group_id, file_name, folder_id, user_id) -> Message:
    msg = Message(media_group_id=media_group_id, file_name=file_name, folder_id=folder_id, user_id=user_id)
    session.add(msg)
    session.commit()
    return msg


def create_folder(name_folder, id_drive_folder) -> Folder:
    folder = Folder(
        name_folder=name_folder,
        id_drive_folder=id_drive_folder,
    )
    session.add(folder)
    session.commit()
    return folder


if __name__ == "__main__":
    for el in session.scalars(get_query_by_media_group_id(69)):
        print(el.file_name)
    create_folder('test_folder3', 'drive_id3')
    create_message(69, 'j.txt', 1, 1)
    create_user('pes')
    print(get_folder_info())
    print(get_message_list_of_user('mot'))
