from src.channel import Channel

class Video(Channel):
    def __init__(self, video_id: str) -> None:
        try:
            video_response = self.get_service().videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                               id=video_id
                                               ).execute()
            self.video_id = video_id
            self.title = video_response['items'][0]['snippet']['title']
            self.url = 'https://www.youtube.com/watch?v=' + video_id
            self.viewCount = video_response['items'][0]['statistics']['viewCount']
            self.like_count = video_response['items'][0]['statistics']['likeCount']
        except IndexError:
            self.title = None
            self.url = None
            self.viewCount = None
            self.like_count = None
        self.video_id = video_id


    def __repr__(self):
        return f"{self.__class__.__name__}({self.video_id}, {self.title}, {self.url}, {self.viewCount})"

    def __str__(self):
        return f"{self.title}"

class PLVideo(Video):
    """Класс для видео на ютуб-канале в плейлисте"""

    def __init__(self, video_id: str, playlist_id: str) -> None:
        """Экземпляр инициализируется id видео и id плейлиста.
        Дальше все данные будут подтягиваться по API."""

        super().__init__(video_id)
        self.playlist_id = playlist_id
