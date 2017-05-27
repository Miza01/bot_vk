import urllib
import requests
import random
import time
from bs4 import BeautifulSoup


# Читает теги из файла tags.txt и выбирает рандомно от 1 до 3. Отдаёт лист с тегами.
def __read_tags_and_check():
    file = open('settings_app/tags.txt', 'r')
    tags = [line.strip() for line in file]  # Выбираем тэги из файла
    print(tags)
    # Выбор тэгов
    number_tags = random.randint(1, 3)  # Выбираем кол-во тэгов от 1 до 3
    choice_tags = []  # Список для выбраных тэгов
    i = 0
    while i != number_tags:
        r = random.choice(tags)
        try:  # Если в choice_tags нет элемента, то записываем его туда
            choice_tags.index(r)
        except ValueError:
            choice_tags.append(r)  # Кидаем элемент в конец списка
        i += 1
    print(choice_tags)
    file.close()  # Закрываем файл
    return choice_tags


# Конект и считывание html. Принимает лист из тэгов. Отдает текст html.
def __connect(list_tags):
    url = 'https://safebooru.org/index.php?page=post&s=list&tags='  # Главный url
    for tag in list_tags:
        url = url + tag + '+'  # Плюсуем тэги
    # Шапка для представления как браузер
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
    }
    html_code = requests.get(url, headers)  # Получаем html
    return html_code.text


# Парсим полученную страницу и отсылаем url с страницы картинки
def __parse_and_get_image_url(html_doc):
    # Выбираем рандомное id
    soup = BeautifulSoup(html_doc, "html.parser")
    div_content = soup.find('div', class_='content')  # Выбираем div.content
    if div_content.find('a') is None:
        time.sleep(3)
        load_img()
    else:
        a = div_content.find_all('a', id=True)  # Ищем все теги <a> с id в div.content
        url_id = random.choice(a)['id']  # Выбираем рандомный id
        url_id = url_id[1:]  # id без первой буквы
        url = "https://safebooru.org/index.php?page=post&s=view&id=" + url_id  # добавляем id в url для перехода к картинке
        return url


# Делаем прямой url картинки
def __get_img_url(url):
    html_code = requests.get(url)  # переходим к картинке
    soup = BeautifulSoup(html_code.text, "html.parser")  # забиваем в суп
    img_url = soup.find('img', id='image')['src']  # ищем
    print('Url картинки: ' + img_url)
    return img_url[2:]


def load_img():
    tags = __read_tags_and_check()
    html = __connect(tags)
    parse = __parse_and_get_image_url(html)
    img_url = __get_img_url(parse)
    img = urllib.request.urlopen("https://" + img_url).read()
    out = open("img/img.jpg", "wb")
    out.write(img)
    out.close()
