# PDS-IAA
This tutorial will guide you through the process of installing, configuring, and using SOFIE's PDS and IAA components.

# Scenario
In this tutorial we consider the following set-up
* A resource server that hosts a resource protected using IAA
* A client wishing to access the resource
* A resource owner acting as the administrator
* An authorization server that generates access tokens.

These entities interact as follows. The resource owner configures the resource server with the DIDs of the authorized
clients. A client authenticates her/him self in the authorization server and obtains a JSON web token (JWT). Then she/he
uses this token to access the protected resource.

# Installation
## Authorization Server
As an authorization server we will use SOFIE's PDS component. 


## Resource server
As an authorization we will use SOFIE's IAA component. 

# Authorization Server configuration
The authorization server needs to configure with the identifiers of the authorized clients. This can be done either manually, or by using PDS administrative interface

## Local configuration
## PDS administrative interface
```python
user = {
    'wallet_config': json.dumps({'id': 'user_wallet',"storage_config":{"path":"tests/indy_wallets"}}),
    'wallet_credentials': json.dumps({'key': 'user_wallet_key'}),
    'did' : '4qk3Ab43ufPQVif4GAzLUW'
}
wallet_handle = await wallet.open_wallet(user['wallet_config'], user['wallet_credentials'])
verkey = await did.key_for_local_did(wallet_handle, user['did'])
nbf = time.mktime(datetime.datetime(2020, 4, 1, 00, 00).timetuple())
exp = time.mktime(datetime.datetime(2020, 4, 1, 23, 59).timetuple()) 
payload = {'action':'add','did':user['did'], 'verkey': verkey, 'metadata':json.dumps({'aud': 'sofie-iot.eu','nbf':nbf, 'exp': exp})}
response  = requests.post("http://localhost:9002/", data = payload).text
response =json.loads(response)
assert(response['code'] == 200)
payload = {'action':'get', 'did':user['did']}
response  = requests.post("http://localhost:9002/", data = payload).text
response =json.loads(response)
assert(response['code'] == 200)
await wallet.close_wallet(wallet_handle)
```

# Client authentication and authorization

```python
user = {
    'wallet_config': json.dumps({'id': 'user_wallet',"storage_config":{"path":"tests/indy_wallets"}}),
    'wallet_credentials': json.dumps({'key': 'user_wallet_key'}),
    'did' : '4qk3Ab43ufPQVif4GAzLUW'
}
payload = {'grant-type':'DID', 'grant':user['did'], 'target':'smartlocker1'}
response  = requests.post("http://localhost:9001/gettoken", data = payload).text
response =json.loads(response)
assert(response['code'] == 401)
challenge = response['challenge']
wallet_handle = await wallet.open_wallet(user['wallet_config'], user['wallet_credentials'])
verkey = await did.key_for_local_did(wallet_handle, user['did'])
signature = await crypto.crypto_sign(wallet_handle, verkey, challenge.encode())
signature64 = base64.b64encode(signature)
exp = time.mktime(datetime.datetime(2020, 4, 1, 23, 59).timetuple())
payload = {'grant-type':'DID', 'grant':user['did'], 'challenge': challenge, 'proof':signature64, 'target':'smartlocker1', 'expires':exp, 'subject': user['did']}
response  = requests.post("http://localhost:9001/gettoken", data = payload).text
response =json.loads(response)
assert(response['code'] == 200)
await wallet.close_wallet(wallet_handle)
```

# Resource access 
```python
token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpZCI6IjM2ZGNlNjBiMzg4YjA2NDUyNmI5MDJhOGRjMzIyM2NhNGMxMWFmNWYiLCJqdGkiOiIzNmRjZTYwYjM4OGIwNjQ1MjZiOTAyYThkYzMyMjNjYTRjMTFhZjVmIiwiaXNzIjoiTktHS3RjTndzc1RvUDVmN3Voc0VzNCIsImF1ZCI6InNvZmllLWlvdC5ldSIsInN1YiI6Im15ZGlkIiwiZXhwIjoxNTgxMzQyNDE4LCJpYXQiOjE1ODEzMzg4MTgsInRva2VuX3R5cGUiOiJiZWFyZXIiLCJzY29wZSI6bnVsbH0.XSyQTgTt1WByT46NJLwrlcU3BUXzWf4MDZE3M4bLAh3HwFAwD6Dhi1IVeLAxNscc0bCgS-3KgyD1fdtiiJH7WktQIc269OLNxhnaXun_LxEYrWQCRHIFb0Je8Eg6CvdOB3shrlNZHmVELe6gaU0tQJ0-cdBbuz0udq_Mou1WLEwe6vp3mfgLiuTe2pT4wVI2PldvmUujeH6IpEop1nESYVA06pK6nV08d1RW7c_sRPgJdpSGGv-QhRcxBjDowkUs9J0OaTtGlExKhMv_17P96EskyOqCHku6RyydFccYbd5tl-Wh-9MqI4Me8z3BBSKPiIvQ2mo5OMcBmI0WwXb6jw"
    payload = {'token-type':'Bearer', 'token':token}
    response  = requests.post("http://localhost:9000/verifytoken", data = payload).text
    response =json.loads(response)
    assert(response['code'] == 200)
```
