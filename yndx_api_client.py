import requests
import os
import json

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
    def __create_json_file(self, file_name, photo_data):
        with open(file_name, 'w') as f:
            json.dump(photo_data, f)

    def __get_url_for_upload(self, file_name):
        params = self.__set_params(file_name)
        response = requests.get(self.__build_url('resources/upload'), headers=self.__set_headers(), params=params)
        print(response.json().get('href'))
        return response.json().get('href')

    def put_folder(self, folder_name):
        params = self.__set_params(folder_name)
        requests.put(self.__build_url('resources'), headers=self.__set_headers(), params=params)    

    def delete_folder(self, folder_name, permanently=False):
        params = self.__set_params(folder_name)
        params.update({'permanently' : permanently})
        requests.delete(self.__build_url('resources'), headers=self.__set_headers(), params=params)

    def post_photo(self, file_name, url):
        params = self.__set_params(file_name)
        params.update({'url' : url})
        requests.post(self.__build_url('resources/upload'), headers=self.__set_headers(), params=params)

    def put_json_file(self, name, photo_data):
        file_name = f'{name}.json'
        self.__create_json_file(file_name, photo_data)
        with open(file_name, 'r') as f:
            requests.put(self.__get_url_for_upload(file_name), files = {'file': f})
        os.remove(f"./{file_name}")
        

if __name__ == '__main__':
    load_dotenv()
    yndx_access_token = os.getenv('YNDX_CLOUD_ACCESS_TOKEN')
    vk_access_token = os.getenv('VK_ACCESS_TOKEN')
    user_id = os.getenv('USER_ID')
    yndx_conn = YNDXAPIClient(yndx_access_token)
    vk_conn = VKAPIClient(vk_access_token, user_id)
    yndx_conn.create_folder('images')
    for photo_array in vk_conn.get_photos():
        photo_url = photo_array.pop('url')
        photo_name = photo_array['file_name']
        file_name = photo_array['file_name'].split('.')[0]
        yndx_conn.put_json_file(file_name, photo_array)
        yndx_conn.post_photo(photo_name, photo_url)
