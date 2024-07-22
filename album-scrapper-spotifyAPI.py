import requests
import env
import csv
 
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
    query = f'q={parsedArtist}%20{parsedAlbum}&type=album,artist,track&limit=30'
    response = requests.get(url=url+query, headers=headers)
    return response

run = True

if run:
    data = GetApiToken()
    print('access_token:', data[0], '\ntokenType:', data[1], '\n')
    headers = {'Authorization': f'{data[1]}  {data[0]}'}


with open('rym_list.csv', 'r', newline='', encoding='utf-8') as arquivo:
    reader = csv.reader(arquivo)

    for coluna in reader:
        l=0
        i=0
        albumDuration = 0 #album time duration (ms)
        artist = coluna[1]
        album = coluna[2]

        print('album:', album, '----->', artist)
        rawData = ApiQuery(album=album, artist=artist, headers=headers)
        data = rawData.json()
        try:
            totaltracks = data['albums']['items'][l]['total_tracks']
            releaseDate = data['albums']['items'][l]['release_date']
            checkList = list(range(totaltracks+1))

            genres = data['artists']['items'][i]['genres']
            popularity = data['artists']['items'][i]['popularity']


            for j in range(30):
                if data['tracks']['items'][j]['album']['name'][:3].lower() == album.lower()[:3]:
                        trackNumber = data['tracks']['items'][j]['track_number']
                        if trackNumber in checkList:
                            albumDuration += data['tracks']['items'][j]['duration_ms']
                            checkList.remove(trackNumber)
        except:
            print('ALGO DEU ERRADO COM O ALBUM:', album, '---->', artist)
            albumDuration=0

        text = album+'--->'+str((albumDuration/60000)/totaltracks)+'\n'
        with open('average-song-durations.txt', 'a', encoding='utf-8') as arquivo:
                arquivo.write(text)

        print('Duracao do album:', albumDuration, '(ms)', 'ou', albumDuration/60000, '(min)')
        print('Total tracks:', totaltracks)
        print('Generos:', genres)
        print('Popularidade:', popularity)
        print('Ano de lancamento:', releaseDate)
        print()
