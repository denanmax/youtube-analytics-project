import json
import os
from googleapiclient.discovery import build
import isodate


# YT_API_KEY скопирован из гугла и вставлен в переменные окружения
api_key: str = os.getenv('YT_API_KEY')
API_KEY = 'AIzaSyCIahIyeqPHc9mVu6VkHB0rJ9zoGjXKKAg'


class Channel:
    """Класс для ютуб-канала"""

    @classmethod
    def get_service(cls):
        """
        Возвращает объект для работы с YouTube API.
        """
        youtube = build('youtube', 'v3', developerKey=API_KEY)
        return youtube

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала.
        Дальше все данные будут подтягиваться по API."""
        # id канала
        # название канала
        # описание канала
        # ссылка на канал
        # количество подписчиков
        # количество видео
        # общее количество просмотров
        channel = Channel.get_service().channels().list(id=channel_id, part='snippet,statistics').execute()
        self._channel_id = channel_id
        self.title = channel['items'][0]['snippet']['title']
        self.description = channel['items'][0]['snippet']['description']
        self.url = channel['items'][0]['snippet']['thumbnails']["default"]['url']
        self.subscriber_count = channel['items'][0]['statistics']['subscriberCount']
        self.video_count = channel['items'][0]['statistics']['videoCount']
        self.viewCount = channel['items'][0]['statistics']['viewCount']

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = Channel.get_service().channels().list(
            id=self.channel_id,
            part='snippet,statistics'
        ).execute()
        info = json.dumps(channel, indent=2, ensure_ascii=False)
        print(info)


    def to_json(self, filename: str) -> None:
        """Сохраняет значения атрибутов экземпляра в файл в формате json."""
        data = {
            "channel_id": self.channel_id,
            "title": self.title,
            "description": self.description,
            "url": self.url,
            "subscriber_count": self.subscriber_count,
            "video_count": self.video_count,
            "viewCount": self.viewCount
        }
        with open(filename, 'w') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    @property
    def channel_id(self) -> str:
        """ Возвращает id канала """
        return self._channel_id
