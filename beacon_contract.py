import requests
# from eth_abi import decode, encode
from config import API_KEY
# import web3

#-------------------------------------
# eth validator index from beaconcha.in
#-------------------------------------
def get_index(api_url, pub_key):
    api_url = "https://beaconcha.in/api/v1/validator/" + str(pub_key)
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        index = data['data']['validatorindex']
        # print ("index: " + str(index))
        return index
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None


#-------------------------------------
# DepositEvent
#-------------------------------------
# def get_deposit_event(api_url, contract_address, API_KEY):
#     params = {
#         'module': 'logs',
#         'action': 'getLogs',
#         'fromBlock': '0',
#         'toBlock': 'latest',
#         'address': contract_address,
#         'topic0': '0x649bbc62d0e31342afea4e5cd82d4049e7e1ee912fc0889aa790803be39038c5',
#         'apikey': API_KEY
#     }
#     response = requests.get(api_url, params=params)
#     if response.status_code == 200:
#         data = response.json()
#         abi = ["bytes", "bytes", "bytes", "bytes", "bytes"]
#         for i in range(len(data['result'])):
#             hex_string = data['result'][i]['data'][2:]
#             data_bytes = bytes.fromhex(hex_string)
#             decoded_data = decode(abi, data_bytes)
#             print ((decoded_data).hex())
#         # print ("get_deposit_event: " + str(data['result']))
#         return data
#     else:
#         print(f"Error: {response.status_code} - {response.text}")
#         return None

# get_deposit_event("https://api.etherscan.io/api", "0x00000000219ab540356cBB839Cbe05303d7705Fa", API_KEY)
