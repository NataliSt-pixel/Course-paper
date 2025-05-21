import requests
import json
from datetime import datetime
import os
from tqdm import tqdm
from urllib.parse import urlparse


class VKPhotoBackup:
    def __init__(self, vk_token, yandex_token, vk_user_id):
        self.vk_token = vk_token
        self.yandex_token = yandex_token
        self.vk_user_id = vk_user_id
        self.vk_api_url = 'https://api.vk.com/method/'
        self.yandex_api_url = 'https://cloud-api.yandex.net/v1/disk/'
        self.headers_yandex = {
            'Authorization': f'OAuth {self.yandex_token}'
        }

    def get_photos(self, album_id='profile', count=5):
        params = {
            'owner_id': self.vk_user_id,
            'album_id': album_id,
            'extended': 1,
            'photo_sizes': 1,
            'count': count,
            'access_token': self.vk_token,
            'v': '5.131'
        }
        response = requests.get(f'{self.vk_api_url}photos.get', params=params)
        if response.status_code != 200 or 'error' in response.json():
            raise Exception(
                f"Ошибка при получении фотографий: {response.json().get('error', {}).get('error_msg', 'Неизвестная ошибка')}")
        return response.json()['response']['items']

    def get_max_size_photo(self, photo):
        sizes = photo['sizes']
        max_size = max(sizes, key=lambda x: x['height'] * x['width'])
        return {
            'url': max_size['url'],
            'type': max_size['type'],
            'likes': photo['likes']['count'],
            'date': photo['date']
        }

    def create_folder(self, folder_name):
        params = {
            'path': folder_name
        }
        response = requests.put(f'{self.yandex_api_url}resources',
                                headers=self.headers_yandex,
                                params=params)
        if response.status_code not in (200, 201, 409):
            raise Exception(f"Ошибка при создании папки: {response.json()}")

    def upload_photo(self, photo_url, file_name, folder_name):
        params = {
            'path': f'{folder_name}/{file_name}',
            'overwrite': True
        }
        response = requests.get(f'{self.yandex_api_url}resources/upload',
                                headers=self.headers_yandex,
                                params=params)

        if response.status_code != 200:
            raise Exception(f"Ошибка при получении URL для загрузки: {response.json()}")

        upload_url = response.json().get('href')
        photo_data = requests.get(photo_url).content
        response = requests.put(upload_url, data=photo_data)

        if response.status_code not in (200, 201):
            raise Exception(f"Ошибка при загрузке файла: {response.text}")

        return response.status_code

    def backup_photos(self, count=5):
        try:
            photos = self.get_photos(count=count)
            if not photos:
                print("Нет фотографий для резервного копирования.")
                return

            photos_info = []
            folder_name = f'VK_Photos_{self.vk_user_id}'

            self.create_folder(folder_name)

            print(f"Начинаем загрузку {len(photos)} фотографий...")

            for photo in tqdm(photos, desc="Загрузка фотографий"):
                max_photo = self.get_max_size_photo(photo)

                file_name = f"{max_photo['likes']}.jpg"

                if any(info['file_name'] == file_name for info in photos_info):
                    date = datetime.fromtimestamp(max_photo['date']).strftime('%Y-%m-%d')
                    file_name = f"{max_photo['likes']}_{date}.jpg"

                self.upload_photo(max_photo['url'], file_name, folder_name)

                photos_info.append({
                    'file_name': file_name,
                    'size': max_photo['type']
                })

            with open('photos_info.json', 'w') as f:
                json.dump(photos_info, f, indent=4)

            print(f"\nРезервное копирование завершено успешно!")
            print(f"Сохранено {len(photos_info)} фотографий в папку '{folder_name}' на Яндекс.Диске.")
            print(f"Информация о фотографиях сохранена в файл 'photos_info.json'.")

        except Exception as e:
            print(f"Произошла ошибка: {str(e)}")


def main():
    print("=== Программа резервного копирования фотографий из VK на Яндекс.Диск ===")

    vk_user_id = input('Введите ID пользователя VK').strip()
    yandex_token = input('Введите токен Яндекс.Диска').strip()
    vk_token = input('Введите токен ВК').strip()

    if not vk_token:
        vk_token = 'Ваш токен VK'

    try:
        backup = VKPhotoBackup(vk_token, yandex_token, vk_user_id)
        count = input("Сколько фотографий сохранить (по умолчанию 5)? ").strip()
        count = int(count) if count.isdigit() else 5
        backup.backup_photos(count)
    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")


if __name__ == '__main__':
    main()