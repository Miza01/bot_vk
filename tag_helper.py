import json
from enum import Enum
from requests_futures.sessions import FuturesSession

class TagCategory(Enum):
    general = 0
    artist = 1
    unknow = 2
    title = 3
    character = 4

__tags = {}

def load_tags_categories(tags):
    url = 'https://safebooru.donmai.us/tags.json?search[name_matches]={}'
    async_session = FuturesSession(max_workers=10)
    futures = []
    for tag in tags:
        futures.append(async_session.get(url.format(tag)))
    
    for future in futures:
        responce = future.result()
        json_array = json.loads(responce.text)
        tag_info = json_array[0]
        tag_name = tag_info["name"]
        tag_category = TagCategory(tag_info["category"])
        __tags[tag_name] = tag_category

def get_tag_category(tag):
    return __tags.get(tag)