import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

response = None

def getUploads(youtube):
    request = youtube.channels().list(
        part="contentDetails",
        mine=True
    )
    results = request.execute()

    for item in results["items"]:
        playlistId = item['contentDetails']['relatedPlaylists']['uploads']
        nextPageToken = ''
        while nextPageToken != None:
            playlistResponse = youtube.playlistItems().list(
                part='contentDetails, snippet',
                playlistId=playlistId,
                pageToken=nextPageToken
            )
            response = playlistResponse.execute()
            print(playlistResponse)

            for playlistItem in response['items']:
                print('[%s] Title: %s'%(
                    playlistItem['snippet']['resourceId']['videoId'],
                    playlistItem['snippet']['title']))
            nextPageToken = response['nextPageToken']

def main():
    channel_id = "UCgyGDGx1ynj7Wtx7DVW-GGQ"
    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "secret.json"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_local_server()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    request = youtube.channels().list(
        part="contentDetails",
        mine=True
    )
    
    getUploads(youtube=youtube)

    return youtube


if __name__ == "__main__":
    main()
