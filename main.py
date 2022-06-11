from source.protocols.vk_protocol import VkProtocol
from source.protocols.ya_protocol import YandexProtocol
from source.uploader import Uploader
from dotenv import load_dotenv
from os import environ


def create_uploader() -> Uploader:
    vk = VkProtocol(environ.get("VK_API_TOKEN"))
    yandex = YandexProtocol(environ.get("YANDEX_API_TOKEN"))

    report = environ.get("REPORT_FILE")

    if report is None:
        report = input("Укажите название файла для отчета >>> ")

    return Uploader(vk, yandex, report)


if __name__ == "__main__":
    load_dotenv()
    uploader = create_uploader()

    user_id = input("Введите id VK пользователя >>> ")
    directory_name = input("Введите название папки >>> ")
    limit = int(input("Введите лимит количества фоток >>> "))

    uploader.download_and_upload_photos(user_id, directory_name, limit)

