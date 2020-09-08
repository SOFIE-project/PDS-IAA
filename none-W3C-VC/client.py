import json
import requests
import base64

'''
A client that uses:
W3C VC as a token
'''

sofie_credential_signed = {
  "@context": [
    "https://www.w3.org/2018/credentials/v1",
    "https://mm.aueb.gr/contexts/access_control/v1"
  ],
  "id": "https://www.sofie-iot.eu/credentials/examples/1",
  "type": [
    "VerifiableCredential"
  ],
  "issuer": "did:nacl:E390CF3B5B93E921C45ED978737D89F61B8CAFF9DE76BFA5F63DA20386BCCA3B",
  "issuanceDate": "2010-01-01T19:23:24Z",
  "credentialSubject": {
    "id": "did:nacl:A490CF3B5B93E921C45ED978737D89F61B8CAFF9DE76BFA5F63DA20386BCCA62",
    "type": [
      "AllowedURLs"
    ],
    "acl": [
      {
        "url": "http://sofie-iot.eu/secure/w3c-vc",
        "methods": [
          "GET",
          "POST"
        ]
      }
    ]
  },
  "proof": {
    "type": "Ed25519Signature2018",
    "created": "2020-08-12T23:21:09Z",
    "verificationMethod": "did:nacl:E390CF3B5B93E921C45ED978737D89F61B8CAFF9DE76BFA5F63DA20386BCCA3B#key0",
    "proofPurpose": "assertionMethod",
    "jws": "eyJhbGciOiJFZERTQSIsImI2NCI6ZmFsc2UsImNyaXQiOlsiYjY0Il19..4XkJwAtDZit6cYb4WoSKPAr8C4ex3NBZnLMAjcETq3TzfBhBQ1HI5tOXhwoZeQdlSmlaMlBzT2E3F9EMIXz0AA"
  }
}

def main():
    print("Client resource access...")
    token = base64.urlsafe_b64encode(json.dumps(sofie_credential_signed).encode()).decode()
    headers = {'Authorization':'Bearer-W3C-VC ' + token, 'Accept': 'application/json'}
    response  = requests.get("http://localhost:9000/secure/w3c-vc", headers = headers).text
    print(response)

if __name__ == '__main__':
    main()