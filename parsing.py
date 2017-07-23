import requests
import random
import time
import json
from lxml import etree
from urllib import request
from bs4 import BeautifulSoup


def __scrap_tag_source(idPost):
    try:
        url = "http://safebooru.org/index.php?page=post&s=view&id=" + str(idPost)
        html = request.urlopen(url).read()
        soup = BeautifulSoup(html, 'html.parser')
        tag = soup.find("li", "tag-type-copyright").a.contents[0]
        tag_parse = "#" + tag.strip().replace(" ", "_").replace("/", " #")
        tagcache_file = open("tagcache.txt", "w")
        tagcache_file.write(tag_parse)
    except:
        tagcache_file = open("tagcache.txt", "w")
        tagcache_file.write("#No_tag")


# Читает теги из файла tags.txt и выбирает рандомно от 1 до 3. Отдаёт лист с тегами.
def __read_tags_and_check():
    file = json.load(open('settings_app/tags.json', "r"))
    tags = file["good"]  # Выбираем тэги из файла
    print(tags)
    # Выбор тэгов
    number_tags = random.randint(1, 3)  # Выбираем кол-во тэгов от 1 до 3
    choice_tags = []  # Список для выбраных тэгов
    i = 0
    while i < number_tags:
        r = random.choice(tags)
        try:  # Если в choice_tags нет элемента, то записываем его туда
            choice_tags.index(r)
        except ValueError:
            choice_tags.append(r)  # Кидаем элемент в конец списка
        i += 1
    print(choice_tags)
    return choice_tags


# Конект и считывание xml.
def __connect(list_tags):
    url = 'https://safebooru.org/index.php?page=dapi&s=post&q=index&tags='  # Главный url
    for tag in list_tags:
        url = url + tag + '+'  # Плюсуем тэги
    # Шапка для представления как браузер
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
    }
    xml = requests.get(url, headers)  # Получаем html
    return xml.text


# Проверка нахождения тега в blacklist
def __check_blacklist(tags):
    file = json.load(open('settings_app/tags.json', "r"))
    blacklist = file["blacklist"]
    for t in blacklist:
        if t in tags:
            return False
    return True


# Парсим полученную страницу и отсылаем url с страницы картинки
def __parse_and_get_image_url(xml):
    root = etree.fromstring(xml.encode())
    if len(root) > 0:
        r = random.randint(0, len(root))
        post = root[r]
        __scrap_tag_source(post.attrib["id"])  # Ищем тег соуса
        if __check_blacklist(post.attrib["tags"]):
            return post.attrib["file_url"][2:]
    time.sleep(3)
    load_img()


def load_img():
    try:
        tags = __read_tags_and_check()
        html = __connect(tags)
        img_url = __parse_and_get_image_url(html)
        img = request.urlopen("https://" + img_url).read()
        out = open("img/img.jpg", "wb")
        out.write(img)
        out.close()
    except Exception as err:
        print(err)
        load_img()
