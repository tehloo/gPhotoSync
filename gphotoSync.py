import os
import json
import pickle
import requests
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

LOG_VERBOSE = True

PATH_SECRET = '.creds'
PATH_TOKEN = PATH_SECRET + '/token.pickle'
PATH_CLIENT_SECRET = PATH_SECRET + '/client_secret.json'

PATH_DUMP_LOG = './log'
DUMP_ALBUM = PATH_DUMP_LOG + '/album.json'
DUMP_MEDIA = PATH_DUMP_LOG + '/media.json'



# Get credentials, refer below
# https://developers.google.com/people/quickstart/python
def getGoogleService():
    cred = None
    if os.path.exists(PATH_TOKEN):
        with open(PATH_TOKEN, 'rb') as token:
            cred = pickle.load(token)

    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            print("Credential exfired. refreshing it.")
            cred.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                PATH_CLIENT_SECRET,
                scopes=['https://www.googleapis.com/auth/photoslibrary.readonly']
            )

            cred = flow.run_local_server(host='localhost',
                port=8080,
                authorization_prompt_message='Please visit this URL: {url}',
                success_message='The auth flow is complete; you may close this window.',
                open_browser=True)

            with open(PATH_TOKEN, 'wb') as token:
                pickle.dump(cred, token)

    # Show credentials for infomation.
    print("Credential : " + str(cred.to_json())) if LOG_VERBOSE else None

    # Get GooglePhoto service
    return build('photoslibrary', 'v1', credentials=cred)


# Get album info
# https://developers.google.com/photos/library/reference/rest/v1/albums/list
def getAlbumIdWithName(service, name):
    resp = service.albums().list().execute()

    strAlbum = json.dumps(resp, sort_keys=True, indent=4)
    with open(DUMP_ALBUM, 'w') as album:
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

    result = {'skip':0, 'download':0, 'error':0}
    while True:
        resp = service.mediaItems().search(body=request).execute()

        # save resp for debugging.
        if LOG_VERBOSE:
            strItems = json.dumps(resp, sort_keys=True, indent=4)
            with open(DUMP_MEDIA, 'w') as items:
                items.write(strItems)

            #print(strItems)

        # ready directory to save files
        if not os.path.exists(path):
            os.mkdir(path)

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

        nextPageToken = resp.get('nextPageToken')
        if nextPageToken:
            request['pageToken'] = nextPageToken
        else:
            break

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

    if LOG_VERBOSE:
        print(f"file saved as {filepath}")

    return True


# Get media items
# https://developers.google.com/photos/library/reference/rest/v1/mediaItems/get
def getMediaItems(service) :
    resp = service.mediaItems().list().execute()

    if LOG_VERBOSE:
        strMedia = json.dumps(resp, sort_keys=True, indent=4)

        with open(DUMP_MEDIA, 'w') as media:
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
PATH_IMAGES = '/home/jckim/Pictures/jay'

# FIXME: make log class later.
if not os.path.exists(PATH_DUMP_LOG):
    os.mkdir(PATH_DUMP_LOG)

service = getGoogleService()
album_id = getAlbumIdWithName(service, ALBUM_NAME_TO_FIND)

if album_id is None:
    print(f"Can not find album '{ALBUM_NAME_TO_FIND}'")
    exit

downloadFilesByAlbumId(service, album_id, PATH_IMAGES)