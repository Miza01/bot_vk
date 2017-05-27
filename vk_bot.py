import vk
import requests
from settings import Settings


def log_in():
    session = vk.AuthSession(app_id=Settings.app_id, user_login=Settings.login, user_password=Settings.password,
                             scope='wall, photos')
    api = vk.API(session)
    return api


def posting():
    api = log_in()  # Логиним API
    upload_url = api.photos.getWallUploadServer(
        group_id=(Settings.owner_id * -1))  # Получаем ссылку для отправки POST запроса
    files = {'photo': open('img/img.jpg', 'rb')}
    req = requests.post(upload_url["upload_url"], files=files)  # Отправляем файл на сервер POST-запросом
    req_json = req.json()  # Парсим полученный после POST-запроса JSON
    photos = api.photos.saveWallPhoto(group_id=(Settings.owner_id * -1), photo=req_json["photo"],
                                      hash=req_json["hash"], server=req_json["server"])  # Сохраняем фотографию
    dict_photo = eval(str(photos)[1::][:-1:])
    api.wall.post(owner_id=Settings.owner_id, message="",
                  attachment=dict_photo['id'])

