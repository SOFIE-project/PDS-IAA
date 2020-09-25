from web3 import Web3
import json

w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:8545"))
with open('ERC721Metadata.bin', 'r') as myfile:
    binfile = myfile.read()
with open('ERC721Metadata.abi', 'r') as myfile:
    abi = myfile.read()

account = w3.eth.accounts[0]
ERC721Contract = w3.eth.contract(abi=abi, bytecode=binfile)
tx_hash = ERC721Contract.constructor("Sofie Access Token", "SAT").transact({'from': account})
tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
address = tx_receipt.contractAddress
print("Contract deployed at " + address)