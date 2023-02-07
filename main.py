import requests
from pprint import pprint
from time import sleep
from tqdm import tqdm
import json


class VkToYa:
    def __init__(self):
        self.ya_token = input('Введите токен от Яндекса: ')
        self.vk_token = input('Введите токен от VK: ')
        self.vk_id = input('Введите id VK: ')
        album_id = int(input('Из какого альбома вы хотите получить фотографии?(Введите номер альбома) '
                             '\n 1 - Фото профиля \n 2 - Фото со стены \n 3 - Сохраненные фото\n'))
        if album_id == 1:
            self.album = 'profile'
        elif album_id == 2:
            self.album = 'wall'
        elif album_id == 3:
            self.album = 'saved'
        self.number_of_photos = int(input('Сколько фото вы хотите загрузить?\n'))

    def upload(self):
        json_data = []
        json_dict = {}
        counter = 0
        for _ in tqdm(self.get_photos()['response']['items']):
            sleep(1)
            if counter == 0:
                requests.put('https://cloud-api.yandex.net/v1/disk/resources', headers=self.get_headers(),
                             params={'path': 'netology'})
            disk_file_path = 'netology/{}'.format(self.get_photos()['response']
                                                  ['items'][counter]['likes']['count'])
            data = self.get_photos()['response']['items'][counter]['sizes'][-1]['url']
            response = requests.post(url="https://cloud-api.yandex.net/v1/disk/resources/upload",
                                     headers=self.get_headers(),
                                     params={'path': disk_file_path,
                                             'url': data})
            json_dict['file_name'] = '{}.jpg'.format(self.get_photos()['response']['items'][counter]['likes']['count'])
            json_dict['size'] = self.get_photos()['response']['items'][counter]['sizes'][-1]['type']
            json_data.append(json_dict)
            json_dict = {}

            counter += 1
        json_object = json.dumps(json_data, indent=2)
        return json_object

    def get_photos(self):
        url = 'https://api.vk.com/method/photos.get'
        params = {
            'owner_id': self.vk_id,
            'access_token': self.vk_token,
            'v': '5.131',
            'extended': '1',
            'photo_sizes': '1',
            'album_id': self.album,
            'count': self.number_of_photos
        }
        result = requests.get(url, params).json()
        return result

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.ya_token)
        }


if __name__ == '__main__':
    uploader = VkToYa()
    pprint(uploader.upload())

