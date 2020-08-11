from indy import did, wallet, crypto
from indy.error import ErrorCode, IndyError
import asyncio
import json
import requests
import base64

'''
A client that uses:
 DID as authorization grant
 JWT as a token
'''

'''
Edit the following variables using the output of the client-setup script
'''
client_did    = '4GZWGKysoekTUN8UJxdoqU'

client = {
    'wallet_config': json.dumps({'id': 'client_wallet', "storage_config":{"path":"."}}),
    'wallet_credentials': json.dumps({'key': 'password'}),
}

async def run():
    print("Commuunicating with PDS...")
    wallet_handle = await wallet.open_wallet(client['wallet_config'], client['wallet_credentials']) 
    payload       = {'grant-type':'DID', 'grant':client_did}
    response      = requests.post("http://localhost:9001/gettoken", data = payload).text
    response      =json.loads(response)
    challenge     = response['challenge']
    print("...Received challenge sending response")
    verkey        = await did.key_for_local_did(wallet_handle, client_did)
    signature     = await crypto.crypto_sign(wallet_handle, verkey, challenge.encode())
    signature64   = base64.b64encode(signature)
    payload       = {'grant-type':'DID', 'grant':client_did, 'challenge': challenge, 'proof':signature64}
    response      = requests.post("http://localhost:9001/gettoken", data = payload).text
    print(response)
    response      = json.loads(response)
    jwt           = response['message']
    print("...Received JWT")
    print(jwt)
    print("Client resource access...")
    headers = {'Authorization':'Bearer ' + jwt, 'Accept': 'application/json'}
    response  = requests.get("http://localhost:9000/secure/jwt", headers = headers).text
    print(response)


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
    loop.close()

if __name__ == '__main__':
    main()