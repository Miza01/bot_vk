import json


def _get_settings():
    file = open('settings_app/setting.json', 'r')
    list_json = json.load(file)
    return list_json


class Settings:
    __list_json = _get_settings()
    login = __list_json["login"]
    password = __list_json["password"]
    api = __list_json["api"]
    owner_id = __list_json["owner_id"]
    app_id = __list_json["app_id"]
