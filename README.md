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
For simplicity reasons we will use the docker images of the SOFIE's components, as well as the included configuration.

**Warning**
> The provided configuration also includes a public/private key pair used for JTW singing/verification. In a real deployment you must use
> your own keys.


## Authorization Server
As an authorization server we will use SOFIE's PDS component. Initially clone the components repository by using:

* git clone https://github.com/SOFIE-project/Privacy-and-Data-Sovereignty.git

Then build the PDS docker image by executing the `docker-build.sh` script


## Resource server
As a resource server we will use SOFIE's IAA component. Therefore, in this tutorial we will not access a real resource, instead we will 
receive a message that the client is authorized to access a resource. Clone IAA repository by using

* git clone https://github.com/SOFIE-project/identity-authentication-authorization.git

Then build the IAA docker image by executing the `docker-build.sh` script

## Client scripts
In order to execute the provided client scripts you will need python3, Hyperledger Indy SDK, and SDK's python3 wrapper. You can install Indy 
SDK and the python3 wrapper by executing the following (assuming you are using Ubuntu 18.04):

* sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys CE7709D068DB5E88
* sudo add-apt-repository "deb https://repo.sovrin.org/sdk/deb bionic stable"
* sudo apt-get update
* sudo apt-get install -y libindy
* pip3 install python3-indy

For other operating systems follow (these instructions)[https://github.com/hyperledger/indy-sdk#installing-the-sdk]

# Execution
Run the PDS and IAA components using the following commands:

* docker run -tid --rm -p 9001-9002:9001-9002 pds
* docker run -tid --rm -p 9000:9000 iaa

## Authorization Server configuration
The authorization server needs to be configured with the identifiers of the authorized clients. This can be done either manually, or by using PDS administrative interface.
First, run the client-setup script (`python3 client-setup.py`). This script will create an Indy wallet, a DID, and a verification key. 

**Note down the output DID and verification key**.

### Configuration using PDS administrative interface
Edit the `owner.py` script by editing the `client_id` and `client_ver_key` variables with the values output by the client-setup.py script. 
Then, run `python3 owner.py` This script configures the PDS component with the client's DID, specifying the period for which the client is authorized,
as well as for which domain. 

## Local configuration
TBP

# Client authentication and authorization, and resource access
Make sure you have executed the previous step and you have configured the authorization server. 
Edit the `client.py` script by editing the `client_id`  variable with the value output by the client-setup.py script.


# Resource access 
```python
token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpZCI6IjM2ZGNlNjBiMzg4YjA2NDUyNmI5MDJhOGRjMzIyM2NhNGMxMWFmNWYiLCJqdGkiOiIzNmRjZTYwYjM4OGIwNjQ1MjZiOTAyYThkYzMyMjNjYTRjMTFhZjVmIiwiaXNzIjoiTktHS3RjTndzc1RvUDVmN3Voc0VzNCIsImF1ZCI6InNvZmllLWlvdC5ldSIsInN1YiI6Im15ZGlkIiwiZXhwIjoxNTgxMzQyNDE4LCJpYXQiOjE1ODEzMzg4MTgsInRva2VuX3R5cGUiOiJiZWFyZXIiLCJzY29wZSI6bnVsbH0.XSyQTgTt1WByT46NJLwrlcU3BUXzWf4MDZE3M4bLAh3HwFAwD6Dhi1IVeLAxNscc0bCgS-3KgyD1fdtiiJH7WktQIc269OLNxhnaXun_LxEYrWQCRHIFb0Je8Eg6CvdOB3shrlNZHmVELe6gaU0tQJ0-cdBbuz0udq_Mou1WLEwe6vp3mfgLiuTe2pT4wVI2PldvmUujeH6IpEop1nESYVA06pK6nV08d1RW7c_sRPgJdpSGGv-QhRcxBjDowkUs9J0OaTtGlExKhMv_17P96EskyOqCHku6RyydFccYbd5tl-Wh-9MqI4Me8z3BBSKPiIvQ2mo5OMcBmI0WwXb6jw"
    payload = {'token-type':'Bearer', 'token':token}
    response  = requests.post("http://localhost:9000/verifytoken", data = payload).text
    response =json.loads(response)
    assert(response['code'] == 200)
```
