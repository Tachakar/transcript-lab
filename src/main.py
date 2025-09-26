import settings as sett
import audio_handler

if __name__ == "__main__":
    settings = sett.Settings()
    sett.prepare_dirs(settings)
    client = audio_handler.YoutubeClient(settings.youtube_api_key)
    data = client.fetch_metadata(
        query="english lessons",
        max_results=2,
        video_duration="medium"
    )
    vid_ids = client.get_vid_ids(data)
    vid_urls = client.get_urls(vid_ids)
    audio_handler.download_wav_files(vid_urls, settings.AUDIO_DIR_PATH)
