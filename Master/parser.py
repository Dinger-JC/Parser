# Parser Industry-Hardstyle-Sex
# Copyright 2026 t.me/Dinger_JC



# Стандартные библиотеки
import json
import math
import os
import random
import re
import string
import sys
from datetime import timedelta
from fractions import Fraction
from pathlib import Path
from pprint import pp
from typing import Any
from urllib.parse import urlparse

# Сторонние библиотеки
import ffmpeg
import yt_dlp
from bs4 import BeautifulSoup
from curl_cffi import requests

# Локальные модули
from logger import Log



class App:
    '''Industry-Hardstyle-Sex'''
    def __init__(self):
        '''Основное'''
        # Проверка необходимых файлов
        self.data: str = 'data.json'
        self.ffmpeg: str = 'ffmpeg.exe'
        self.ffprobe: str = 'ffprobe.exe'
        self.CheckRequiredFiles(self.data, self.ffmpeg, self.ffprobe)

        # Версия Chrome
        self.chrome = '131'

        # Извлечение ссылки
        with open(self.data, encoding = 'utf-8') as file:
            links: dict = json.load(file)
        self.sites: dict = links['sites']
        self.presets: dict = links['videos']

        self.raw: str = input('Введите ссылку или выберите из доступных пресетов: 1, 2, 3, 4\n').strip()

        if self.raw in links.get('videos', {}):
            self.url: str = self.presets[self.raw]
        else:
            self.url = self.raw

        self.domain: str = urlparse(self.url).netloc

        log.info(f'Ссылка: {self.url}')
        log.info(f'Сайт: {self.domain}')

        # Директория
        self.name_folder: str = 'Saved Videos'
        self.folder: Path = Path(__file__).parent / self.name_folder
        self.folder.mkdir(parents = True, exist_ok = True)

        # Название кэша
        self.symbols: str = string.ascii_letters + string.digits + '_' * 5 + '-' * 5
        self.filename: str = ''.join(random.choice(self.symbols) for _ in range(32))
        self.file: str = f'{self.folder / self.filename}.mp4'

        # Заголовки HTTP-запросов
        self.headers: dict = {
            'user-agent': f'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{self.chrome}.0.0.0 Safari/537.36', # Имитация браузера Chrome (TLS/HTTP2) для обхода защиты
            'referer': f'https://{self.domain}/', # Указывает серверу, с какой страницы пришел запрос
            'accept-language': 'ru,en-US;q=0.9,en;q=0.8', # Языки
            'sec-ch-ua': f'"Not(A:Brand";v="99", "Google Chrome";v="{self.chrome}", "Chromium";v="{self.chrome}"', # Движок
            'sec-ch-ua-mobile': '?0', # Платформа
            'sec-ch-ua-platform': '"Windows"', # ОС
            'sec-fetch-mode': 'no-cors', # Режим запроса без CORS
            'sec-fetch-site': 'cross-site' # Запрос идет на другой домен
        }

        # Настройки для yt_dlp
        self.yt_dlp_options: dict = {
            'http_headers': self.headers, # Заголовки HTTP-запросов
            'progress_hooks': [self.ProgressBar], # Отслеживание прогресса загрузки
            'ffmpeg_location': str(Path(__file__).parent.absolute() / self.ffmpeg), # Путь ffmpeg
            'outtmpl': self.file, # Путь сохраняемого файла
            'format': 'bestvideo+bestaudio/best', # Качество видео
            'merge_output_format': 'mp4', # Формат после загрузки
            'socket_timeout': 15, # Время ожидания ответа от сервера (в секундах)
            'sleep_interval': 0, # Минимальная случайная пауза между загрузками (в секундах)
            'max_sleep_interval': 2, # Максимальная случайная пауза между запросами (в секундах)
            'retries': 3, # Количество попыток переподключения при ошибке загрузки файла
            'fragment_retries': 3, # Количество попыток загрузки каждого отдельного фрагмента видео
            'rm_cached_metadata': True, # Очистка метаданных из кэша перед началом загрузки
            'nocheckcertificate': True, # Игнорировать ошибки проверки SSL-сертификатов
            'quiet': True, # Лог
            'verbose': False # Подробный лог
        }

        # Настройки для ffprobe
        self.ffprobe_options: dict = {
            'headers': ''.join([f'{k}: {v}\r\n' for k, v in self.headers.items()]), # Заголовки HTTP-запросов
            'analyzeduration': '5000000', # Время на чтение данных (в микросекундах)
            'probesize': '5000000', # Максимальный объем данных для анализа (в микросекундах)
            'rw_timeout': '10000000', # Общее время на операцию (в микросекундах)
            'reconnect_delay_max': '5', # Максимальное время ожидания (в секундах)
            'tls_verify': '0', # Отключает проверку SSL-сертификатов
            'reconnect': '1', # Автоматическое переподключение
            'seekable': '0', # Чтение потока последовательно
            'reconnect_streamed': '1' # Автоматическое переподключение для стримов
        }

        self.GetInfo(self.url, self.domain, self.sites)
        self.GetVideo(self.video_url)

    def CheckRequiredFiles(self, data: str, ffmpeg: str, ffprobe: str):
        '''Проверка наличия необходимых файлов'''
        link: str = 'https://github.com/GyanD/codexffmpeg/releases/tag/2026-01-05-git-2892815c45'
        error: bool = False

        if not os.path.exists(ffmpeg):
            log.error(f'Файл "{ffmpeg}" не найден. Для необходимой работы скачайте его здесь: {link}.')
            error = True

        if not os.path.exists(ffprobe):
            log.error(f'Файл "{ffprobe}" не найден. Для необходимой работы скачайте его здесь: {link}.')
            error = True

        if not os.path.exists(data):
            log.error(f'Файл "{data}" не найден. Для необходимой работы создайте его по инструкции в README.')
            error = True

        if error:
            sys.exit(0)

    def FormatUnits(self, value: int, format: str = '') -> str:
        '''Конвертация байтов'''
        factor: dict = {
            'KiB': 1024,
            'MiB': 1024 ** 2,
            'GiB': 1024 ** 3
        }

        if value is None or value == 0:
            return 'N/A'

        if value < factor['KiB']:
            return f'{value} B' + format

        if value < factor['MiB']:
            return f'{value / factor['KiB']:.3f} KiB' + format

        if value < factor['GiB']:
            return f'{value / factor['MiB']:.3f} MiB' + format

        return f'{value / factor['GiB']:.3f} GiB' + format

    def ProgressBar(self, data: Any):
        '''Индикатор загрузки'''
        if data['status'] == 'downloading':
            speed: int = data.get('speed')
            volume: int = data.get('total_bytes') or data.get('total_bytes_estimate')
            downloaded: int = data.get('downloaded_bytes', 0)
            percent: float = round(downloaded / volume * 100, 2)

            print(
                f'\r[СКАЧИВАНИЕ] '
                f'Прогресс: {percent:.2f}% | '
                f'Скорость: {self.FormatUnits(speed, '/s')} | '
                f'Размер: {self.FormatUnits(volume)}', end = ''
            )

        elif data['status'] == 'finished':
            counter = 1
            while True:
                new_name: str = Path(self.folder) / f'{self.site} Video-{counter}.mp4'
                if not new_name.exists():
                    os.rename(self.file, new_name)
                    break
                counter += 1
            log.info(f'Видео успешно скачалось ({self.folder}).')

    def CheckLink(self, response: str) -> str:
        '''Проверка ответа страницы'''
        code: int = response.status_code
        errors: dict = {
            400: 'некорректный запрос. Проверьте правильность введенных данных.',
            401: 'требуется авторизация. Войдите в аккаунт, чтобы получить доступ.',
            403: 'доступ запрещён. Сервер отклонил запрос.',
            404: 'страница не найдена. Проверьте адрес или она была удалена.',
            408: 'время ожидания истекло. Сервер слишком долго ждал ответа.',
            429: 'слишком много запросов. Вы превысили лимит, подождите немного.',
            500: 'внутрненняя ошибка сервера. На сервере что-то пошло не так',
            502: 'ошибка соединения. Сервер получил некорректный ответ от вышестоящего узла.',
            503: 'сервер временно перегружен. Технические работы или высокая нагрузка.'
        }

        if code in [200, 206]:
            return
        else:
            log.error(f'Ошибка [{code}] {errors.get(code, errors.keys())}')
            sys.exit(0)

    def GetResolution(self, width: int, height: int) -> str:
        '''Получение типа разрешения'''
        quality_types: dict = {
            'LD': [426, 240],
            'SD': [640, 360],
            'HD': [1280, 720],
            'Full HD': [1920, 1080],
            '2K Quad HD': [2560, 1440]
        }

        if [width, height] == quality_types['SD']:
            return f'SD {width}x{height}'

        elif [width, height] == quality_types['HD']:
            return f'HD {width}x{height}'

        elif [width, height] == quality_types['Full HD']:
            return f'Full HD {width}x{height}'

        elif [width, height] == quality_types['2K Quad HD']:
            return f'2K Quad HD {width}x{height}'

        else:
            return f'Другое {width}x{height}'

    def GetInfo(self, url: str, domain: str, sites: dict):
        '''Получение данных с сайта'''
        # Проверка ссылки
        if not re.search(r'video|watch', url):
            log.error(f'Некорректная ссылка. По этой ссылке не удалось найти видео.')
            sys.exit(0)

        # Проверка сайта
        try:
            response = requests.get(url, timeout = 15, impersonate = f'chrome{self.chrome}')
            self.CheckLink(response)

        except requests.exceptions.ConnectionError:
            log.error(f'Ошибка подключения к {domain}. Ресурс может быть заблокирован или требовать прокси/VPN.')
            sys.exit(0)

        except requests.exceptions.Timeout:
            log.error(f'Превышено время ожидания ответа от {domain}.')
            sys.exit(0)

        page = BeautifulSoup(response.text, 'html.parser')
        self.video_url: str = None

        # Проверка домена
        if domain == sites['Strip2']:
            raw_title: str = page.find('title').text
            title: str = re.sub(r'\s*[-–—]\s*Strip2.co\s*$', '', raw_title, flags = re.IGNORECASE).strip()
            self.site: str = 'Strip2'

            links = []
            self.video_url = page.find_all('a', href = True)
            for link in self.video_url:
                if 'vps402.strip2.co.mp4' in link['href']:
                    links.append(link['href'])

            for i, href in enumerate(links):
                find_link: str = str(href)
                if find_link and f'/x{len(links) - 1}/' in find_link:
                    self.video_url: str = find_link

        elif domain == sites['AnalMedia']:
            raw_title: str = page.find('title').text
            title: str = re.sub(r'\s*[-–—]\s*AnalMedia\s*$', '', raw_title, flags = re.IGNORECASE).strip()
            self.site: str = 'AnalMedia'

            video: str = page.find('video')
            self.video_url: str = video.find('source')['src']

        else:
            log.error('Загрузка со сторонних ресурсов невозможна. Cкачивание возможно только с Strip2 и AnalMedia.')
            sys.exit(0)

        log.info(f'Название: {title}')
        log.info(f'Прямая ссылка: {self.video_url}')

        # Получение дополнительной информации
        video_info: dict = ffmpeg.probe(self.video_url, **self.ffprobe_options)
        video_stream: dict = next((stream for stream in video_info['streams'] if stream['codec_type'] == 'video'), None)
        width: int = video_stream.get('width', 0)
        height: int = video_stream.get('height', 0)
        log.info(f'Разрешение: {self.GetResolution(width, height)}')

        fps: int = math.ceil(float(Fraction(video_stream.get('avg_frame_rate', 'N/A'))))
        log.info(f'FPS: {fps}')

        duration: str = video_stream.get('duration', 'N/A')
        duration: str = str(timedelta(seconds = float(video_stream.get('duration')))).split('.')[0]
        log.info(f'Длительность: {duration}')

    def GetVideo(self, video_url: str):
        '''Скачивание видео'''
        log.info('Видео начало скачиваться')
        with yt_dlp.YoutubeDL(self.yt_dlp_options) as video:
            video.download([video_url])



if __name__ == '__main__':
    try:
        log = Log(__name__)
        log.info('Запуск')
        app = App()

    except Exception as error:
        log.error(f'Непредвиденная ошибка: {error}')
