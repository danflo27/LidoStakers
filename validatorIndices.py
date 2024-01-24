# loop through the 39 lido node operators

# for each operator, get the list of added validators

import requests
from eth_abi import decode
import sha3
from config import API_KEY 
from web3 import Web3

api_url = "https://api.etherscan.io/api" 
contract_address = "0x55032650b14df07b85bF18A3a3eC8E0Af2e028d5"

#_______________________________________________________________________________________________________________________
# getActiveNodeOperatorsCount()
#_______________________________________________________________________________________________________________________
k = sha3.keccak_256()
k.update(b"getActiveNodeOperatorsCount()")
getActiveNodeOperatorsCount = "0x" + k.hexdigest()

params = {
    'module': 'proxy',
    'action': 'eth_call',
    'to': contract_address,
    'data': getActiveNodeOperatorsCount,
    'apikey': API_KEY
}
response = requests.get(api_url, params=params)
if response.status_code == 200:
    data = response.json()
else:
    print(f"Error: {response.status_code} - {response.text}")

numberOfOperators = int(data['result'], 16)
print ("numberOfOperators: " + str(numberOfOperators))

#_______________________________________________________________________________________________________________________
# getActiveNodeOperator(uint256,bool)
#_______________________________________________________________________________________________________________________
k = sha3.keccak_256()
k.update(b"getNodeOperator(uint256,bool)")
getNodeOperator = "0x" + k.hexdigest()[:8]

# Encode the parameters
params_encoded = Web3.eth.encodeABI(parameters=[1, True], types=['uint256', 'bool']) # not working

# Append the encoded parameters to the function signature
getNodeOperator += params_encoded

params = {
    'module': 'proxy',
    'action': 'eth_call',
    'to': contract_address,
    'data': getNodeOperator,
    'apikey': API_KEY
}
response = requests.get(api_url, params=params)
if response.status_code == 200:
    data = response.json()
else:
    print(f"Error: {response.status_code} - {response.text}")

abi = ["bool","string","address","uint256","uint256","uint256","uint256"]
hex_string = data['result'][2:]
decoded_data = decode(abi, bytes.fromhex(hex_string))
print ("getNodeOperator: " + str(decoded_data))


