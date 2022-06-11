import requests
from .vk_protocol import UserPhoto


class YandexProtocol:
    url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
    token: str
    headers: dict
    _cache: dict

    def __init__(self, token) -> None:
        self.token = token
        self.headers = {'Authorization': f'OAuth {token}'}
        self._cache = {}

        assert self.token != "", "Укажите токен для работы с API YANDEX"

    def upload_to_directory(self, target_folder: str, user_photo: UserPhoto) -> None:
        self._init_folder(target_folder)

        params = {
            'path': '/'.join([target_folder, user_photo.get_filename()]),
            'url': user_photo.url,
        }

        response = requests.post(self.url, params=params, headers=self.headers)
        response.raise_for_status()

        if response.status_code in (201, 202):
            pass #print(f"Success -{params}")

        return response

    def _init_folder(self, target_folder):
        if self._cache.get(target_folder) is not None:
            return

        url = 'https://cloud-api.yandex.net/v1/disk/resources?path=' + target_folder
        response = requests.put(url, headers=self.headers)

        self._cache[target_folder] = True

        if response.status_code == 201:
            print(f'\nПапка {target_folder} создана на Яндекс диске\n')
        elif response.status_code == 409:
            print(f'\nПапка {target_folder} существует.\n')
        else:
            print('Ошибка')