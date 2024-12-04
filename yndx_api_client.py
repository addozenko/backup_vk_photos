import requests
import os

from dotenv import load_dotenv
from pprint import pprint

from vk_api_client import VKAPIClient


class YNDXAPIClient:

    BASE_URL = 'https://cloud-api.yandex.net/v1/disk/'

    def __init__(self, token):
        self.token = token

    def __build_url(self, api_method):
        return f'{self.BASE_URL}{api_method}'
    
    def __set_headers(self):
        headers = {
            'Authorization' : self.token
        } 
        return headers

    def __set_params(self, path):
        params = {
            'path' : path, 
        }
        return params
    
    def create_folder(self, folder_name):
        params = self.__set_params(folder_name)
        requests.put(self.__build_url('resources'), headers=self.__set_headers(), params=params)

    def delete_folder(self, folder_name, permanently=False):
        params = self.__set_params(folder_name)
        params.update({'permanently' : permanently})
        requests.delete(self.__build_url('resources'), headers=self.__set_headers(), params=params)

    def set_photo(self, filename, url):
        params = self.__set_params(filename)
        params.update({'url' : url})
        requests.post(self.__build_url('resources/upload'), headers=self.__set_headers(), params=params)

if __name__ == '__main__':
    load_dotenv()
    yndx_access_token = os.getenv('YNDX_CLOUD_ACCESS_TOKEN')
    vk_access_token = os.getenv('VK_ACCESS_TOKEN')
    user_id = os.getenv('USER_ID')
    yndx_conn = YNDXAPIClient(yndx_access_token)
    vk_conn = VKAPIClient(vk_access_token, user_id)
    for photo_array in vk_conn.get_photos():
        photo_url = photo_array.pop('url')
        photo_name = photo_array['file_name']
        yndx_conn.set_photo(photo_name, photo_url)
