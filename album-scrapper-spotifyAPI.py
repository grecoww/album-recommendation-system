import requests
import env
 
def GetApiToken():
    authentication = f'grant_type=client_credentials&client_id={env.clientId}&client_secret={env.clientSecret}'
    rawTokenInfo = requests.post(url='https://accounts.spotify.com/api/token', headers={'Content-Type': 'application/x-www-form-urlencoded'}, data=authentication)
    TokenInfo = rawTokenInfo.json()
    accessToken = TokenInfo['access_token']
    tokenType = TokenInfo['token_type']
    return (accessToken, tokenType)

def ApiQuery(album, artist, headers):
    parsedAlbum = requests.utils.quote(album)
    parsedArtist = requests.utils.quote(artist)
    url = 'https://api.spotify.com/v1/search?'
    query = f'q={parsedAlbum}album:{parsedAlbum}artist:{parsedArtist}&type=artist,track'
    response = requests.get(url=url+query, headers=headers)
    return response.text

run = True

if run:
    data = GetApiToken()
    print('access_token:', data[0], '\ntokenType:', data[1])
    headers = {'Authorization': f'{data[1]}  {data[0]}'}


with open('RYMdata.txt', 'r') as arquivo:
    for query in arquivo:
        (album, artist) = query.split(' - ')
        print('album:', album, '----->', artist)
        rawData = ApiQuery(album=album, artist=artist, headers=headers)
        with open('ParsedRYMdata.txt', 'w') as escritor:
            escritor.write(rawData)
