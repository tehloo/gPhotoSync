import os
import json
import pickle
import requests
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

# Get credentials, refer below
# https://developers.google.com/people/quickstart/python
def getGoogleService():
    cred = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            cred = pickle.load(token)

    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret.json',
                scopes=['https://www.googleapis.com/auth/photoslibrary.readonly']
            )

            cred = flow.run_local_server(host='localhost',
                port=8080,
                authorization_prompt_message='Please visit this URL: {url}',
                success_message='The auth flow is complete; you may close this window.',
                open_browser=True)

            with open('token.pickle', 'wb') as token:
                pickle.dump(cred, token)

    # Show credentials for infomation.
    print ("Credential : " + str(cred.to_json()))

    # Get GooglePhoto service
    return build('photoslibrary', 'v1', credentials=cred)


# Get album info
# https://developers.google.com/photos/library/reference/rest/v1/albums/list
def getAlbumIdWithName(service, name):
    resp = service.albums().list().execute()

    strAlbum = json.dumps(resp, sort_keys=True, indent=4)
    with open('album.json', 'w') as album:
        album.write(strAlbum)

    #print(strAlbum)
    print("\n Receive album infomation completed!!!\n")

    # Find out album id by the name of it.
    for album in resp.get('albums'):
        if album.get('title') == name:
            return album.get('id')


def downloadFilesByAlbumId(service, album_id, path):
    request = {
        'albumId' : album_id,
        'pageSize' : 100
    }
    resp = service.mediaItems().search(body=request).execute()

    # save resp for debugging.
    strItems = json.dumps(resp, sort_keys=True, indent=4)
    with open('items.json', 'w') as items:
        items.write(strItems)

    #print(strItems)

    # ready directory to save files
    if not os.path.exists(path):
        os.mkdir(path)

    result = {'skip':0, 'download':0, 'error':0}
    for item in resp.get('mediaItems'):
        filepath = path + '/' + item.get('filename')
        url = item.get('baseUrl') + '=d'

        if os.path.exists(filepath):
            print("File exist. " + filepath)
            result['skip'] += 1
        elif downloadFileWithUrl(url, filepath):
            result['download'] += 1
        else:
            result['error'] += 1

    print("download completed.")
    print(f" + download {result['download']} files") if result['download'] else None
    print(f" + skip {result['skip']} files") if result['skip'] else None
    print(f" + error {result['error']}") if result['error'] else None


def downloadFileWithUrl(url, filepath):
    with open(filepath, 'wb') as f:
        response = requests.get(url, stream=True)

        if not response.ok:
            print(response)
            return False

        for block in response.iter_content(1024):
            if not block:
                break
            f.write(block)

    print(f"file saved as {filepath}")
    return True


# Get media items
# https://developers.google.com/photos/library/reference/rest/v1/mediaItems/get
def getMediaItems(service) :
    resp = service.mediaItems().list().execute()
    strMedia = json.dumps(resp, sort_keys=True, indent=4)

    with open('media.json', 'w') as media:
        media.write(strMedia)

    print("\n Receive completed!!!\n")
    print(strMedia)

    # Get single items from list
    for item in resp.get('mediaItems'):
        filename = item.get("filename")
        url = item.get('baseUrl')
        url += '=d'
        downloadFileWithUrl(url, filename)



ALBUM_NAME_TO_FIND = 'jay'
PATH_IMAGES = './images'

service = getGoogleService()
album_id = getAlbumIdWithName(service, ALBUM_NAME_TO_FIND)

if album_id is None:
    print(f"Can not find album '{ALBUM_NAME_TO_FIND}'")
    exit

downloadFilesByAlbumId(service, album_id, PATH_IMAGES)