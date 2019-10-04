from bottle import route
from bottle import run
from bottle import HTTPError
from bottle import request
import album_search

@route("/albums/<artist>")
def albums(artist):
    albums_list = album_search.find(artist)
    if not albums_list[0]:
        message = "Альбомов {} не найдено".format(artist)
        result = HTTPError(404, message)
    else:
        album_names = [album.album for album in albums_list[0]]
        result = "Всего найдено {} альбомов группы {}:<br> ".format(albums_list[1],artist)
        result += "<br>".join(album_names)
    return result

@route("/albums", method="POST")
def save_my_data():
    year = request.forms.get('year')
    artist = request.forms.get('artist')
    genre = request.forms.get('genre')
    album = request.forms.get('album')
    try:
        year = int(year)
    except ValueError:
        return HTTPError(400, "год введен не числом")
    try:
        album_search.valid_data(year, artist,genre, album)
    except (album_search.albium_err, album_search.genre_err, album_search.artist_err, album_search.year_err) as err:
        return HTTPError(400,err)
    except (album_search.duplicate_album) as err:
        return HTTPError(409,err)
    else:
        user_data = {
            'year': year,
            'artist': artist,
            'genre': genre,
            'album': album
        }
        album_search.save_data(user_data)
        return "Данные успешно сохранены"

if __name__ == "__main__":
    run(host="localhost", port=8080, debug=True)

#для проверки можно использовать ниже запросы. При необходимости поправить их
#http://localhost:8080/albums/Beatles
#http -f POST localhost:8080/albums year='1992' artist='Tranwek' genre='rock' album='Saernd'
