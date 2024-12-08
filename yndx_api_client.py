import requests
import os
import json


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
        return response.json().get('href')

    def __get_folder_info(self, folder_name):
        params = self.__set_params(folder_name)
        responce = requests.get(self.__build_url('resources'), headers=self.__set_headers(), params=params)
        return responce.json()

    def create_folder(self, folder_name):
        params = self.__set_params(folder_name)
        requests.put(self.__build_url('resources'), headers=self.__set_headers(), params=params) 
        print(f'Создал папку - {folder_name}') 

    def delete_folder(self, folder_name, permanently=False):
        params = self.__set_params(folder_name)
        params.update({'permanently' : permanently})
        requests.delete(self.__build_url('resources'), headers=self.__set_headers(), params=params)
        print(f'Удалил папку - {folder_name}') 

    def post_photo(self, file_name, url, folder_name = 'vk_images'):
        if self.__get_folder_info(folder_name).get('error') == 'DiskNotFoundError':
            self.create_folder(folder_name)
        params = self.__set_params(f'{folder_name}/{file_name}')
        params.update({'url' : url})
        requests.post(self.__build_url('resources/upload'), headers=self.__set_headers(), params=params)
        print(f'Загрузил фотографию - {folder_name}/{file_name}') 

    def put_json_file(self, name, photo_array, folder_name = 'vk_images'):
        if self.__get_folder_info(folder_name).get('error') == 'DiskNotFoundError':
            self.create_folder(folder_name) 
        file_name = f'{name}.json'
        self.__create_json_file(file_name, photo_array)
        with open(file_name, 'r') as f:
            requests.put(self.__get_url_for_upload(f'{folder_name}/{file_name}'), files = {'file': f})
            print(f'Загрузил файл - {folder_name}/{file_name}') 
        os.remove(f"./{file_name}")
        

if __name__ == '__main__':
    pass
