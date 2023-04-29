import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

# PTmmMssS to seconds
def durationCalc(time):
    try:
        parts = time.strip("PT").split("M")
        minutes = int(parts[0])
        if len(parts) == 2:
            seconds = int(parts[1].strip("S"))
        else:
            seconds = 0 
        return minutes*60 + seconds
    except ValueError:
        print(f"value {time} is not compatible and probably not part of a real match")
        return 0

def getVideoInfo(youtube, videoId):

    request = youtube.videos().list(
        part="snippet,contentDetails,fileDetails",
        id=videoId
    )

    response = request.execute()['items'][0]
    return {
        'title': response['snippet']['title'],
        'fileName' : response['fileDetails']['fileName'],
        'duration': durationCalc(response['contentDetails']['duration']),
        'uploadDate': response['snippet']['publishedAt']
    }


def getUploadsFromPlaylist(youtube, playlistId, title):
    ret = {
        'title': title,
        'videos': []
    }

    nextPageToken = ''
    while nextPageToken != None:
        request = youtube.playlistItems().list(
            part="snippet",
            playlistId=playlistId,
            pageToken=nextPageToken
        )
        response = request.execute()

        for playlistItem in response['items']:
            ret['videos'].append(
                getVideoInfo(youtube,
                    playlistItem['snippet']['resourceId']['videoId']
                )
            )

        try:
            nextPageToken = response["nextPageToken"]
        except KeyError:
            nextPageToken = None
    return ret

def getAllPlaylists(youtube):
    ret = {
        'channel': '',
        'playlists': []
    }
    request = youtube.channels().list(
        part="snippet",
        mine=True
    )

    channelResp = request.execute()

    ret['channel'] = channelResp['items'][0]['snippet']['title']

    nextPageToken = ''
    while nextPageToken != None:
        request = youtube.playlists().list(
            part="contentDetails, snippet",
            mine=True,
            pageToken=nextPageToken
        )
        playlistResults = request.execute()
        for playlistItem in playlistResults['items']:
            playlistId = playlistItem['id']
            title = playlistItem['snippet']['title']
            ret['playlists'].append(
                getUploadsFromPlaylist(youtube, playlistId, title)
            )

        try:
            nextPageToken = playlistResults['nextPageToken']
        except KeyError:
            nextPageToken = None
    return ret

def getYoutube():
    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "secret.json"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_local_server()
    return googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)