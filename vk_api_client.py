import requests
import os

from dotenv import load_dotenv
from pprint import pprint
from urllib.parse import urlencode


class VKAPIClient:

    BASE_URL = 'https://api.vk.com/method/'

    def __init__(self, token, user_id, version = '5.199'):
        self.token = token
        self.user_id = user_id
        self.version = version

    def __get_common_params(self):
        return {
            'access_token' : self.token,
            'v' : self.version,
            'offline' : 0
        }
    
    def __build_url(self, api_method):
        return f'{self.BASE_URL}/{api_method}'

    def __get_largest_photo(self, photos_array):
        result = []
        for items in photos_array['response']['items']:
            data = dict.fromkeys(['file_name', 'size', 'url'])
            data['file_name'] = f"{items['likes']['count']}.jpg"
            largest_photo = sorted(items['sizes'], key=lambda d: d['height'])[-1]
            data['size'] = largest_photo['type']
            data['url'] = largest_photo['url']
            result.append(data)
        return result

    def photos_get(self):
        params = self.__get_common_params()
        params.update({'owner_id' : self.user_id, 'album_id' : 'profile', 'photo_sizes': 1, 'extended' : 1})
        response = requests.get(self.__build_url('photos.get'), params=params)
        return self.__get_largest_photo(response.json())
    
load_dotenv()
access_token = os.getenv('ACCESS_TOKEN')
user_id = os.getenv('USER_ID')
client = VKAPIClient(access_token, user_id)
output = client.photos_get()
pprint(output)