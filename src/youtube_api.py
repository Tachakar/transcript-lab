import googleapiclient.discovery
import logging

class YoutubeClient():
    def __init__(self, api_key:str):
        self.api_key = api_key
        self.youtube_client = googleapiclient.discovery.build(serviceName="youtube",version="v3",developerKey=self.api_key)

    def fetch_metadata(
        self,
        query: str,
        max_results: int = 1,
        video_duration: str = "medium",
    ):
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

    def get_vid_ids(self, data:dict) -> list:
        ids = []
        for vid in data['items']:
            ids.append(vid['id']['videoId'])
        return ids

