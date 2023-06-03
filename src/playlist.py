from src.channel import Channel
import isodate, datetime
import os
api_key: str = os.getenv('YT_API_KEY')
class PlayList():
    def __init__(self, playlist_id):
        """Получить данные по play-листам канала"""
        youtube = Channel.get_service()
        playlist_request = youtube.playlists().list(
            part='snippet',
            id=playlist_id,
            maxResults=50
        )
        self.playlist_respond = playlist_request.execute() # проверяю вывод словаря
        self.playlist_id = playlist_id
        self.title = self.playlist_respond['items'][0]['snippet']['title']
        self.url = f'https://www.youtube.com/playlist?list={playlist_id}'
        playlist_videos = Channel.get_service().playlistItems().list(playlistId=playlist_id,
                                                                     part='contentDetails',
                                                                     maxResults=50,
                                                                     ).execute()
        playlist_video_ids = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        self.video_response = Channel.get_service().videos().list(part='contentDetails,statistics',
                                                                  id=','.join(playlist_video_ids)
                                                                  ).execute()

    @property
    def total_duration(self):
        '''Возвращает объект класса datetime.timedelta с суммарной длительность плейлиста (обращение как к свойству)'''
        total_duration = datetime.timedelta(seconds=0)
        for video in self.video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_duration += duration

        return total_duration

    def show_best_video(self):
        '''Возвращает ссылку на самое популярное видео из плейлиста (по количеству лайков)'''
        greatest_likes = 0
        greatest_video = ''
        for video in self.video_response['items']:
            if int(video['statistics']['likeCount']) > greatest_likes:
                greatest_video = video['id']
        return f"https://youtu.be/{greatest_video}"
