import os

from dotenv import load_dotenv

from vk_api_client import VKAPIClient
from yndx_api_client import YNDXAPIClient


load_dotenv()
yndx_access_token = os.getenv('YNDX_CLOUD_ACCESS_TOKEN')
vk_access_token = os.getenv('VK_ACCESS_TOKEN')
user_id = os.getenv('USER_ID')
yndx_conn = YNDXAPIClient(yndx_access_token)
vk_conn = VKAPIClient(vk_access_token, user_id)
for photo_array in vk_conn.get_photos():
    photo_url = photo_array.pop('url')
    photo_name = photo_array['file_name']
    file_name = photo_array['file_name'].split('.')[0]
    yndx_conn.put_json_file(file_name, photo_array)
    yndx_conn.post_photo(photo_name, photo_url)