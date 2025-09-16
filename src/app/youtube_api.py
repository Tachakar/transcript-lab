from settings import settings
import googleapiclient.discovery

def fetch_metadata():
    youtube_client = googleapiclient.discovery.build(serviceName="youtube",version="v3",developerKey=settings.youtube_api_key)
    request = youtube_client.search().list(
        type="video",
        part="snippet",
        q="language lessons",
        videoDuration = "medium",
        videoLicense = "creativeCommon",
        maxResults = 2
    )
    data = request.execute()
    print(data)

fetch_metadata()
