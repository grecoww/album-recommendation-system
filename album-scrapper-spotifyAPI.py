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
    query = f'q={parsedAlbum}%2520album:{parsedAlbum}%2520artist:{parsedArtist}&type=artist,track'
    response = requests.get(url=url+query, headers=headers)
    return response

run = True

if run:
    data = GetApiToken()
    print('access_token:', data[0], '\ntokenType:', data[1], '\n')
    headers = {'Authorization': f'{data[1]}  {data[0]}'}


with open('RYMdata.txt', 'r') as arquivo:
    for linha in arquivo:
        i=0
        l=0
        albumDuration = 0 #album time duration (ms)
        (album, artist) = linha.strip().split(' - ')
        print('album:', album, '----->', artist)
        rawData = ApiQuery(album=album, artist=artist, headers=headers)
        data = rawData.json()

        while data['artists']['items'][i]['name'] != artist:
            i+=1
        print('A pesquisa efetiva foi no artista de index:', i)
        genres = data['artists']['items'][i]['genres']
        popularity = data['artists']['items'][i]['popularity']


        while data['tracks']['items'][l]['album']['name'] != album:
            l+=1
        totaltracks = data['tracks']['items'][l]['album']['total_tracks']
        releaseDate = data['tracks']['items'][l]['album']['release_date']
        checkList = list(range(totaltracks+1))

        for j in range(20):
            if data['tracks']['items'][j]['album']['name'] == album:
                    trackNumber = data['tracks']['items'][j]['track_number']
                    if trackNumber in checkList:
                        albumDuration += data['tracks']['items'][j]['duration_ms']
                        checkList.remove(trackNumber)

        print('Duracao do album:', albumDuration, '(ms)', 'ou', albumDuration/60000, '(min)')
        print('Generos:', genres)
        print('Popularidade:', popularity)
        print('Total Tracks', totaltracks)
        print('Ano de lancamento:', releaseDate)
        print()


        #with open('ParsedRYMdata.txt', 'w') as escritor:
        #   escritor.write(rawData)
