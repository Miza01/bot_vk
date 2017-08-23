import requests
import random
import time
import json
import tag_helper
from tag_helper import TagCategory
from lxml import etree
from urllib import request
from bs4 import BeautifulSoup


#
# NullSanya part
#

def __load_tags_from_json():
    print('Load tags from file')
    json_file = open("settings_app/tags.json")
    json_object = json.load(json_file)
    json_file.close()
    return json_object

def __get_random_tags(whitelist):
    print('Get random tags')
    length = len(whitelist)
    tags_count = random.randint(1, min([3, length]))
    tags = []
    for i in range(0, tags_count):
        random_tag = random.choice(whitelist)
        while random_tag in tags:
            random_tag = random.choice(whitelist)
        tags.append(random_tag)
    print('Tags for search: {}'.format(tags))
    return tags

def __get_api_link_to_posts(whitelist, blacklist):
    print('Get api link to posts')
    url = 'https://safebooru.org/index.php?page=dapi&s=post&q=index&tags={}&json=1'
    bl = list(map(lambda tag: '-' + tag, blacklist))
    tags = '+'.join(whitelist + bl)
    return url.format(tags)

def __get_image_json(url):
    print('Get image json')
    response = requests.get(url)
    json_array = json.loads(response.text)
    count = len(json_array)
    r = random.randint(0, count - 1)
    return json_array[r]

def __get_info_about_image(image_json):
    print('Get image info from json')
    tags = image_json['tags'].split(' ')
    tag_helper.load_tags_categories(tags)
    image_info = { TagCategory.artist : [], TagCategory.title : [], TagCategory.character : [], TagCategory.general : [] }
    for tag in tags:
        tag_category = tag_helper.get_tag_category(tag)
        image_info[tag_category].append(tag)
    return image_info

def __get_link_to_image_file(image_json):
    print('Get image link from json')
    url = 'https://safebooru.org/images/{}/{}'
    directory = image_json['directory']
    image = image_json['image']
    return url.format(directory, image)

def __safe_image_to_file(image_url, filename):
    print('Safe image to file')
    image_bytes = request.urlopen(image_url).read()
    file = open(filename, "wb")
    file.write(image_bytes)
    file.close()

def __safe_message_in_file(image_info):
    print('Safe message to file')
    message_template = 'Title: {}\nCharacters: {}\nArtist: {}'
    titles = ', '.join(image_info[TagCategory.title])
    artists = ', '.join(image_info[TagCategory.artist])
    characters = ', '.join(image_info[TagCategory.character])
    message = message_template.format(titles, characters, artists)
    message_file = open("tagcache.txt", "w")
    message_file.write(message)
    message_file.close()

#
# end NullSanya part
#

def load_img():
    try:
        tags = __load_tags_from_json()
        random_tags = __get_random_tags(tags["good"])
        api_link = __get_api_link_to_posts(random_tags, tags['blacklist'])
        image_json = __get_image_json(api_link)
        image_info = __get_info_about_image(image_json)
        image_link = __get_link_to_image_file(image_json)
        __safe_message_in_file(image_info)
        __safe_image_to_file(image_link, 'img/img.jpg')
    except Exception as err:
        print(err)
        load_img()
