import requests
import env
 
def GetApiToken():
    authentication = f'grant_type=client_credentials&client_id={env.clientId}&client_secret={env.clientSecret}'
    rawTokenInfo = requests.post(url='https://accounts.spotify.com/api/token', headers={'Content-Type': 'application/x-www-form-urlencoded'}, data=authentication)
    accessToken = rawTokenInfo["access_token"]
    tokenType = rawTokenInfo["token_type"]
    return {accessToken, tokenType}

run = True

if run:
    data = GetApiToken()
    print(data)


url = 'https://api.spotify.com/v1/search?'
headers = {'Authorization': f'{data.tokenType} {data.accessToken}'}

with open('RYMdata.txt', 'r') as arquivo:
    for i in arquivo:
        print(i)
        album = ''
        artist = ''
        query = f'q=album:{album}%20artist:{artist}&type=album'
        response = requests.get(url=url+query, headers=headers)
        with open('parsedRYMdata.txt', 'w') as escritor:
            escritor.write(response.text)