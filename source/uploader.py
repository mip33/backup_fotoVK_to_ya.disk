import json
from tqdm import tqdm
from .protocols.vk_protocol import UserPhoto, VkProtocol
from .protocols.ya_protocol import YandexProtocol


class Uploader:
    vk: VkProtocol
    yandex: YandexProtocol
    report_file: str

    def __init__(self, vk, yandex, report_file: str) -> None:
        self.vk = vk
        self.yandex = yandex
        self.report_file = report_file

    def download_and_upload_photos(self, user_id: str, target_folder: str, limit: int):
        photos = self.vk.get_user_photos(user_id, limit)

        for x in tqdm(photos):
            self.yandex.upload_to_directory(target_folder, x)

        self._write_report(photos)

    def _write_report(self, uploaded_photos: list[UserPhoto]):
        output = []

        for ph in uploaded_photos:
            photo_result = {
                'file_name': ph.get_filename(),
                'size': ph.size
            }

            output.append(photo_result)

        with open(self.report_file, 'w', encoding='utf8') as f:
            json.dump(output, f)