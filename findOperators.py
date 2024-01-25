# for each operator, get the list of added validators
import requests
from eth_abi import decode, encode
import sha3
from config import API_KEY

api_url = "https://api.etherscan.io/api" 
contract_address = "0x55032650b14df07b85bF18A3a3eC8E0Af2e028d5"

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
        print ("numberOfOperators: " + str(numberOfOperators))
        return numberOfOperators
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None
    
#-------------------------------------
# getActiveNodeOperator(uint256,bool)
#-------------------------------------
def get_node_operator(api_url, contract_address, API_KEY, operator_id):
    k = sha3.keccak_256()
    k.update(b"getNodeOperator(uint256,bool)")
    getNodeOperator = "0x" + k.hexdigest()[:8]

    params_encoded = encode(['uint256', 'bool'], [operator_id, True]).hex()
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
        print ("get_node_operator " + str(operator_id) + ":" + str(decoded_data))
        return decoded_data
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None
