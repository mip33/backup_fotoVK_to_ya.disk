import os
import requests

VK_SIZE_MAP = {'s': 0, 'm': 1, 'x': 2, 'o': 3, 'p': 4, 'q': 5, 'r': 6, 'y': 7, 'z': 8, 'w': 9}

class UserPhoto:
    url: str
    size: str
    likes: int
    date: str

    def __init__(self, size, url, likes, date) -> None:
        self.size = size
        self.url = url
        self.likes = likes
        self.date = date

    def get_filename(self) -> str:
        base = os.path.basename(self.url)
        name_without_query = base.split('?')[0]
        _, extension = name_without_query.split(".")

        return f"{self.likes}.{self.date}.{extension}"

class VkProtocol:
    url = "https://api.vk.com/method/"
    token: str
    default_params: dict

    def __init__(self, token, version="5.131") -> None:
        self.token = token
        self.default_params = {
            'access_token': token,
            'v': version
        }

        assert self.token != "", "Укажите токен для работы с API VK"

    def get_user_photos(self, user_id: str, limit: int) -> list[UserPhoto]:
        response = self._request(
            'photos.get', 
            {
                'album_id': 'profile',
                'extended': 1,
                'photo_sizes': 1,
                'feed_type': 'photo',
                'count': limit,
                'owner_id': user_id
            }
        )

        photos_data = response['response']['items']
        photos_objects = []

        for ph in photos_data:
            photo_object = self._get_maximum_size_by_photo(ph)
            photos_objects.append(photo_object)

        return photos_objects

    def _request(self, method: str, params: dict) -> dict:
        return requests.get(
            f"{self.url}/{method}", 
            params={**self.default_params, **params}
        ).json()

    def _get_maximum_size_by_photo(self, photo: dict) -> UserPhoto:
        sort_size = sorted(
            photo['sizes'], 
            key=lambda x: VK_SIZE_MAP[x['type']], 
            reverse=True
        )

        found = sort_size[0]

        return UserPhoto(
            found['type'],
            found['url'],
            photo['likes']['count'],
            photo['date']
        )