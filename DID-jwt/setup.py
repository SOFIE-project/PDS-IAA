from indy import did, wallet
from indy.error import ErrorCode, IndyError
import asyncio
import json

client = {
    'wallet_config': json.dumps({'id': 'client_wallet', "storage_config":{"path":"."}}),
    'wallet_credentials': json.dumps({'key': 'password'}),
}

async def setup():
    print("Creating client wallet and DID...")
    try:
        await wallet.create_wallet(client['wallet_config'], client['wallet_credentials'])
    except IndyError as ex:
        if ex.error_code == ErrorCode.WalletAlreadyExistsError:
            pass
    wallet_handle             = await wallet.open_wallet(client['wallet_config'], client['wallet_credentials']) 
    client_did, client_verkey = await did.create_and_store_my_did(wallet_handle,"{}")
    print("DID: " + client_did)
    print("Verification key: " + client_verkey)
    await wallet.close_wallet(wallet_handle)
    print("Creating configuration file for the example")
    conf = {}
    conf['client_did']    = client_did
    conf['client_verkey'] = client_verkey
    with open('did-jwt-example.conf', 'w') as f:
        json.dump(conf,f)

def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(setup())
    loop.close()

if __name__ == '__main__':
    main()