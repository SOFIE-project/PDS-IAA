import json
import requests
import base64

'''
A client that uses:
Authorization code as authorization grant
JWT as a token
'''

def main():
    print("Communicating with PDS...")
    payload = {'grant-type':'auth_code', 'grant':'shared_secret_key', 'metadata':json.dumps({'aud': 'sofie-iot.eu'}), 'erc-721':'True'}
    response  = requests.post("http://localhost:9001/gettoken", data = payload)
    jwt       = response.text
    print("...Received JWT")
    print(jwt)
    print("Client resource access...")
    headers = {'Authorization':'Bearer ' + jwt, 'Accept': 'application/json'}
    response  = requests.get("http://localhost:9000/secure/jwt", headers = headers).text
    print(response)

if __name__ == '__main__':
    main()