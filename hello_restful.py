import requests

API_HOST = 'https://photoslibrary.googleapis.com'
headers = {'Authorization': 'Bearer [YOUR_ACCESS_TOKEN]'}

def req(path, query, method, data={}):
    url = API_HOST + path
    print('HTTP Method: %s' % method)
    print('Request URL: %s' % url)
    print('Headers: %s' % headers)
    print('QueryString: %s' % query)

    if method == 'GET':
        return requests.get(url, headers=headers)
    else:
        return requests.post(url, headers=headers, data=data)

resp = req('/v1/albums', '', 'GET')
print("response status:\n%d" % resp.status_code)
print("response headers:\n%s" % resp.headers)
print("response body:\n%s" % resp.text)
