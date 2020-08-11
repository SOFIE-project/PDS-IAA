import requests
import datetime
import time
import json

'''
Edit the following variables using the output of the client-setup script
'''
client_did    = '4GZWGKysoekTUN8UJxdoqU'
client_verkey = '2nKNxt27d2TpmHR3fWqsc2ebKjTYfXauJzMiFC8fAGud'

'''
The following fields will be used when constructing the JWT for that client
'''
nbf = time.mktime(datetime.datetime(2020, 4, 1, 00, 00).timetuple()) # Not before 
exp = time.mktime(datetime.datetime(2020, 4, 1, 23, 59).timetuple()) # Expiration time
aud = 'sofie-iot.eu'                                                 # The domain name of the protected resourse


payload = {'action':'add','did':client_did, 'verkey': client_verkey , 'metadata':json.dumps({'aud':aud ,'nbf':nbf, 'exp': exp})}
response = requests.post("http://localhost:9002/", data = payload).text
response = json.loads(response)
print(response)