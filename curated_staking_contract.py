# for each operator, get the list of added validators
import requests
from eth_abi import decode, encode
import sha3
from config import API_KEY

#-------------------------------------
# getActiveNodeOperatorsCount()
#-------------------------------------
def get_number_of_operators(api_url, contract_address, API_KEY):
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
        numberOfOperators = int(data['result'], 16)
        print ("\nnumber of node operators: " + str(numberOfOperators) + "\n")
        return numberOfOperators
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None
    
#-------------------------------------
# getActiveNodeOperator(uint256,bool)
#-------------------------------------
def get_node_operator(api_url, contract_address, API_KEY, _nodeOperatorId):
    k = sha3.keccak_256()
    k.update(b"getNodeOperator(uint256,bool)")
    getNodeOperator = "0x" + k.hexdigest()[:8]

    params_encoded = encode(['uint256', 'bool'], [_nodeOperatorId, True]).hex()
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
        abi = ["bool","string","address","uint256","uint256","uint256","uint256"]
        hex_string = data['result'][2:]
        decoded_data = decode(abi, bytes.fromhex(hex_string))
        print ("node operator " + str(_nodeOperatorId) + ":" + str(decoded_data))
        return decoded_data
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

#-------------------------------------
# getSigningKeys(uint256)
#-------------------------------------
def get_signing_key(api_url, contract_address, API_KEY, _nodeOperatorId, _index):
    k = sha3.keccak_256()
    k.update(b"getSigningKey(uint256,uint256)")
    getSigningKey = "0x" + k.hexdigest()[:8]

    params_encoded = encode(['uint256', 'uint256'], [_nodeOperatorId, _index]).hex()
    getSigningKey += params_encoded

    params = {
        'module': 'proxy',
        'action': 'eth_call',
        'to': contract_address,
        'data': getSigningKey,
        'apikey': API_KEY
    }
    response = requests.get(api_url, params=params)
    if response.status_code == 200:
        data = response.json()
        abi = ["bytes","bytes","bool"]
        hex_string = data['result'][2:]
        decoded_data = decode(abi, bytes.fromhex(hex_string))
        deposit_signature = decoded_data[1].hex()
        key = decoded_data[0].hex()
        return deposit_signature, key, _index
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None