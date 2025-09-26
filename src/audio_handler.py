from pathlib import Path
import yt_dlp
import googleapiclient.discovery
import logging


class YoutubeClient():
    def __init__(self, api_key:str) -> None:
        self.api_key = api_key
        self.youtube_client = googleapiclient.discovery.build(serviceName="youtube",version="v3",developerKey=self.api_key)

    def fetch_metadata(
        self,
        query: str,
        max_results: int = 1,
        video_duration: str = "medium",
    ) -> dict:
        try:
            request = self.youtube_client.search().list(
                type="video",
                part="snippet",
                q=query,
                videoDuration = video_duration,
                videoLicense = "creativeCommon",
                maxResults = max_results
            )
            return request.execute()

        except Exception as e:
            logging.warning(f"Something went wrong. LOG: {e}")
            return {}

    def get_vid_ids(self, data:dict) -> list[str]:
        ids = []
        for vid in data['items']:
            ids.append(vid['id']['videoId'])
        return ids

    def get_urls(self, vid_ids: list[str]) -> list[str]:
        urls = []
        base_url = "https://www.youtube.com/watch?v="
        for id in vid_ids:
            urls.append(base_url+id)
        return urls


def download_wav_files(urls: list[str], path: Path) -> None:
    YDL_OPTS = {
        "format": "bestaudio/best",
        "outtmpl": str(path/"%(id)s.%(ext)s"),
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec":"wav",
            "preferredquality": "0",
        }],
    }

    with yt_dlp.YoutubeDL(YDL_OPTS) as ydl:
        ydl.download(urls)
