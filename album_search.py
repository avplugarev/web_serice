"""
#TODO: Веб-сервер принимает GET-запросы по адресу /albums/<artist> и выводит на экран сообщение с
количеством альбомов исполнителя artist и списком названий этих альбомов..

Если артист artist не зарегистрирован в музыкальной коллекции, то есть в базе данных отсутствуют
соответствующие записи, сервер возвращает 404 ошибку.
"""
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base



DB_PATH = "sqlite:///albums.sqlite3"
Base = declarative_base()

class Album(Base):
    """
    Описывает структуру таблицы album для хранения записей музыкальной библиотеки
    """

    __tablename__ = "album"

    id = sa.Column(sa.INTEGER, primary_key=True)
    year = sa.Column(sa.INTEGER)
    artist = sa.Column(sa.TEXT)
    genre = sa.Column(sa.TEXT)
    album = sa.Column(sa.TEXT)

class user_data_err(ValueError):
    """
    Общий класс на ощиюки связанные с заполнением данных и их сохранением
    """
    pass
class year_err(user_data_err):
    """
    Некорректно заполнен год
    """
    pass
class albium_err(user_data_err):
    """
    Некорректно заполнено название альбома
    """
    pass
class genre_err (user_data_err):
    """
    Некорректно заполнен жанр
    """
    pass
class artist_err (user_data_err):
    """
    Некорректно заполнено имя артиста
    """
    pass
class duplicate_album (user_data_err):
    """
    Проверак на наличие уже в базе дубля альбома
    """
    pass


def connect_db():
    """
    Устанавливает соединение к базе данных, создает таблицы, если их еще нет и возвращает объект сессии
    """
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()

def valid_data(year, artist,genre, album):
    """
    проверяем корректность вводимых данных
    """

    if isinstance(year, int) is False:
        raise year_err ("год введен не числом")
    if isinstance(artist, str) is False:
        raise artist_err ("некорректно введен артист")
    if isinstance(genre, str) is False:
        raise genre_err("некорректно введен жанр")
    if isinstance(album, str) is False:
        raise albium_err("некорректно введен альбом")

    session = connect_db()

    duplicate_new_album=session.query(Album).filter(Album.artist == artist,
                                                    Album.year==year,
                                                    Album.genre==genre,
                                                    Album.album ==album).first()
    if duplicate_new_album is not None:
        raise duplicate_album("Такой альбом уже есть")
    return True

def find(artist):
    """
    Находит все альбомы в базе данных по заданному артисту
    """
    session = connect_db()
    albums = session.query(Album).filter(Album.artist == artist).all()
    albums_count=len(albums)
    return albums, albums_count

def save_data(data):
    """
    Сохраняем данные в базу данных
    """
    session = connect_db()

    new_album=Album(
        year=data['year'],
        artist=data['artist'],
        genre=data['genre'],
        album=data['album']
    )
    session.add(new_album)
    session.commit()
    print("Спасибо, данные сохранены!")

