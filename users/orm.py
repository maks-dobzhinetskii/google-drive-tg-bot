from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.selectable import Select

from users.models import Message, UserInfo, Folder
from users.database import engine


Session = sessionmaker(bind=engine)
session = Session()


def get_query_by_media_group_id(media_group_id: int) -> Select:
    return select(Message).where(Message.media_group_id == media_group_id)


def get_message_list_of_user(username: str) -> str:
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


def get_message_info(id_drive_folder: int) -> Select:
    return (
        session.query(Message)
        .join(Folder, Folder.id == Message.folder_id)
        .where(Folder.id_drive_folder == id_drive_folder)
        .first()
    )


def get_folder_info_by_username(username: str):
    return (
        session.query(Folder)
        .join(Message, Folder.id == Message.folder_id)
        .join(UserInfo, UserInfo.id == Message.user_id)
        .where(UserInfo.username == username)
        .all()
    )


def get_folder_info_by_id_drive_folder(id_drive_folder: str) -> Select:
    return (
        session.query(Folder).where(Folder.id_drive_folder == id_drive_folder).first()
    )


def get_user_info(username):
    return session.query(UserInfo).where(UserInfo.username == username).first()


def create_user(username: str) -> UserInfo:
    user = UserInfo(username=username)
    session.add(user)
    session.commit()
    return user


def create_message(media_group_id, file_name, folder_id, user_id) -> Message:
    msg = Message(
        media_group_id=media_group_id,
        file_name=file_name,
        folder_id=folder_id,
        user_id=user_id,
    )
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
    create_folder('qq', '123')
    create_message(69, 'j.txt', 1, 1)
    create_user('gg')
    print(get_folder_info())
    print(get_message_list_of_user('mot'))
    print(get_user_info('gg').username)
    print(get_message_info('123').file_name)
    print(get_folder_info_by_username("pes").name_folder)
