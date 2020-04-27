import requests
import datetime
import time
import json

'''
Edit the following variables using the output of the client-setup script
'''
client_did    = '7FJs8MXbdTTmWx3HNyfMRN'
client_verkey = '4QUGgBZDpnHXHa1gJ3rTNhQcCwC94DjFt5iSwgQ3dbVm'

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