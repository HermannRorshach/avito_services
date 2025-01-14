import os
import sys
from io import BytesIO
from random import shuffle

import boto3
import openpyxl
from botocore.config import Config
from dotenv import load_dotenv

# Загрузка переменных окружения
if hasattr(sys, '_MEIPASS'):
    env_path = os.path.join(sys._MEIPASS, '.env')
else:
    env_path = '.env'

load_dotenv(env_path)

YANDEX_ACCESS_KEY = os.getenv('YANDEX_CLOUD_ACCESS_KEY_ID')
YANDEX_SECRET_KEY = os.getenv('YANDEX_CLOUD_SECRET_ACCESS_KEY')
YANDEX_ENDPOINT_URL = 'https://storage.yandexcloud.net'

# Настройка клиента S3
session = boto3.session.Session()
s3_client = session.client(
    service_name='s3',
    endpoint_url=YANDEX_ENDPOINT_URL,
    aws_access_key_id=YANDEX_ACCESS_KEY,
    aws_secret_access_key=YANDEX_SECRET_KEY,
    config=Config(signature_version='s3v4', max_pool_connections=50)
)

class Paths:
    def __init__(self):
        self.full_paths = []  # Полные пути
        self.relative_paths = []  # Относительные пути

    def add_full_path(self, full_path):
        self.full_paths.append(full_path)

    def extend_full_paths(self, full_paths_list):
        self.full_paths.extend(full_paths_list)

    def add_relative_path(self, relative_path):
        self.relative_paths.append(relative_path)

    def extend_relative_paths(self, relative_paths_list):
        self.relative_paths.extend(relative_paths_list)


def get_files(bucket_name):
    files = Paths()
    try:
        # Инициализируем переменную для токена пагинации
        continuation_token = None

        while True:
            # Выполняем запрос с возможным токеном продолжения
            if continuation_token:
                response = s3_client.list_objects_v2(
                    Bucket=bucket_name,
                    ContinuationToken=continuation_token
                )
            else:
                response = s3_client.list_objects_v2(Bucket=bucket_name)

            if 'Contents' in response:
                for obj in response['Contents']:
                    if not obj['Key'].endswith('/'):  # Исключаем папки
                        filename = obj['Key']
                        files.add_relative_path(filename)
                        files.add_full_path(f"{YANDEX_ENDPOINT_URL}/{bucket_name}/{filename}")

            # Если есть токен продолжения, запрашиваем следующую страницу
            if response.get('IsTruncated'):  # Если объекты не все, продолжаем с токеном
                continuation_token = response.get('NextContinuationToken')
            else:
                break  # Если объекты закончились, выходим из цикла

    except Exception as e:
        print(f"Ошибка при получении списка файлов: {e}")

    print(f"Длина списка файлов в бакете: {len(files.relative_paths)}")
    return files


def get_directories(files, obj, index, name):
    try:
        for file in files.relative_paths:
            folder = '/'.join(file.split('/')[:index])
            if not folder in obj.relative_paths:
                obj.add_relative_path(folder)

        for file in files.full_paths:
            folder = '/'.join(file.split('/')[:index])
            if not folder in obj.full_paths:
                obj.add_full_path(folder)
    except Exception as e:
        print(f"Ошибка при получении списка {name}: {e}")

    return obj



def update_excel_with_image_urls(bucket_name, file_obj, sheet_name):
    files = get_files(bucket_name)

    folders = Paths()
    folders = get_directories(files, folders, -1, "папок")

    products = Paths()
    products = get_directories(files, products, -2, "продуктов")

    categories = Paths()
    categories = get_directories(files, categories, -3, "категорий")
    shuffle(files.relative_paths)

    category_images = [
        [
        [
            [
                f"{YANDEX_ENDPOINT_URL}/{bucket_name}/{file}" for file in files.relative_paths
                if file.startswith(folder + "/")
            ]
            for folder in folders.relative_paths
            if folder.startswith(product + "/")
        ]
        for product in products.relative_paths
        if product.startswith(category + "/")
        ]
        for category in categories.relative_paths
    ]

    values_for_table = []
    for category in category_images:
        for product in category:
            values_for_table.extend([" | ".join(items) for items in zip(*product)])
        values_for_table.append("")

    wb = openpyxl.load_workbook(file_obj)


    # Открытие нужного листа
    sheet = wb[sheet_name]

    # Найдём индекс столбца с названием "ImageUrls"
    header_row = sheet[1]  # Предполагаем, что заголовки находятся в первой строке
    image_urls_column = None
    for col_idx, cell in enumerate(header_row, 1):
        if cell.value == "ImageUrls":
            image_urls_column = col_idx
            break

    if image_urls_column is None:
        raise ValueError("Столбец 'ImageUrls' не найден.")

    # Заполнение столбца "ImageUrls"
    row_idx = 4  # Начинаем с 2-й строки (после заголовка)
    for i, image_url in enumerate(values_for_table):
        sheet.cell(row=row_idx, column=image_urls_column, value=image_url)
        row_idx += 1

    output = BytesIO()
    wb.save(output)
    output.seek(0)
    wb.close()
    return output


if __name__ == "__main__":
    bucket_name = input("Введите имя бакета\n") # "0001-small-test"
    file_name = input("Введите имя файла Excel, в который нужно записать ссылки\n") # "ggdevice.xlsx"
    sheet_name = input("Введите имя страницы\n") # "2"

    output = update_excel_with_image_urls(bucket_name, file_name, sheet_name)
    with open(file_name, 'wb') as f:
        f.write(output.read())
    print(f"Файл {file_name} успешно обновлён, ссылки записаны")