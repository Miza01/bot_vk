import requests
import random
from bs4 import BeautifulSoup


# Читает теги из файла tags.txt и выбирает рандомно от 1 до 3. Отдаёт лист с тегами.
def read_tags_and_check():
    file = open('tags.txt', 'r')
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
    file.close()  # Закрываем файл
    return choice_tags


# Конект и считывание html. Принимает лист из тэгов. Отдает текст html.
def connect(list_tags):
    url = 'https://safebooru.org/index.php?page=post&s=list&tags='  # Главный url
    for tag in list_tags:
        url = url + tag + '+'  # Плюсуем тэги
    # Шапка для представления как браузер
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
    }

    html_code = requests.get(url, headers)  # Получаем html

    with open('test.html', 'w') as output_file:  # Записываем полученный html
        output_file.write(html_code.text)
    html_code = html_code.text
    return html_code


def parse_and_get_image_url(html_doc):
    # Выбираем рандомное id
    soup = BeautifulSoup(''.join(html_doc))
    div_content = soup.find('div', class_='content')  # Выбираем div.content
    if div_content is None:
        get_images()
    else:
        a = div_content.find_all('a')  # Ищем все теги a в div.content
        id = a[random.randint(0, 40)]['id']  # Выбираем рандомный id
        id = id[1:]  # id без первой буквы
        url = "https://safebooru.org/index.php?page=post&s=view&id=" + id  # добавляем id в url для перехода к картинке
        return url


def get_img_url(url):
    html_code = requests.get(url)  # переходим к картинке
    soup = BeautifulSoup(html_code.text)  # забиваем в суп
    img_url = soup.find('img', id='image')['src']  # ищем
    return img_url[2:]


def get_images():
    tags = read_tags_and_check()
    html = connect(tags)
    parse = parse_and_get_image_url(html)
    img_url = get_img_url(parse)
    print(img_url)


get_images()
