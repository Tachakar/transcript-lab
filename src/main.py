import settings as sett
import youtube_api

if __name__ == "__main__":
    settings = sett.Settings()
    sett.prepare_dirs(settings)
    client = youtube_api.YoutubeClient(settings.youtube_api_key)
    data = client.fetch_metadata(
        query="english lessons",
        max_results=2,
        video_duration="medium"
    )
