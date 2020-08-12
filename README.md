# PDS-IAA
This repository includes examples of using SOFIE's
[PDS](https://github.com/SOFIE-project/Privacy-and-Data-Sovereignty) and [IAA](https://github.com/SOFIE-project/identity-authentication-authorization) components. 

# Examples setup
Figure 1 shows the setup of our examples. PDS acts as an OAuth2.0 authorization server
that accepts as input an authorization grant, and outputs access tokens. IAA acts
as a forward proxy, it receives HTTP requests that include the access token, and if
the token is valid it forwards the request to appropriate endpoint. Additionally, we
consider (and provide) an "owner" component which is used for configuring PDS, as well
as a "resource" component which is protected by IAA. The following example vary 
depending on the type of authorization grants and of access tokens. 

# Installation
For simplicity reasons we will use the docker images of the SOFIE's components, as well as the included configuration.

**Warning**
> The provided configuration also includes a public/private key pair used for JTW singing/verification. In a real deployment you must use
> your own keys.


## PDS
Initially clone the components repository by using:

* git clone https://github.com/SOFIE-project/Privacy-and-Data-Sovereignty.git

Then build the PDS docker image by executing the `docker-build.sh` script


## IAA
Clone IAA repository by using

* git clone https://github.com/SOFIE-project/identity-authentication-authorization.git

Then build the IAA docker image by executing the `docker-build.sh` script

## Client, Owner, Server, and Setup script
In order to execute the auxilliary scripts you will need python3, Hyperledger Indy SDK, and SDK's python3 wrapper. You can install Indy 
SDK and the python3 wrapper by executing the following (assuming you are using Ubuntu 18.04):

* sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys CE7709D068DB5E88
* sudo add-apt-repository "deb https://repo.sovrin.org/sdk/deb bionic stable"
* sudo apt-get update
* sudo apt-get install -y libindy
* pip3 install python3-indy

For other operating systems follow [these instructions](https://github.com/hyperledger/indy-sdk#installing-the-sdk)

# Example 1: Hyperldger DID authorization grant and JWT access token
This example is located in the folder DID-jwt

## Preparation
Run the setup script

* python3 setup.py

The script created a Hyperledger Indy wallet for the client, it generates a DID and a verification key,
and records the latter information in a configuration file (names did-jwt-example.conf). This configuration 
is later used by the "owner" script in order to configure PDS.

## Execution

Run the PDS and IAA components using the following commands:

* docker run -tid --rm -p 9001-9002:9001-9002 pds
* docker run -tid --rm -p 9000:9000 --network="host"  iaa

(note that --network="host" is used because the resource server runs in localhost, otherwise it is not needed)

Run the resource server

* python3 server.py

Run the owner script in order to configure PDS, with the client's DID, specifying the period for which the client is authorized, as well as for which domain

* python3 owner.py

Finally run the client script. The client script interacts with PDS, it receives an access token, and then 
interacts with the resource server through IAA.

* python3 client.py



