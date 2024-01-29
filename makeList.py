from curated_staking_contract import get_node_operator, get_number_of_operators, get_signing_key, API_KEY
from beacon_contract import get_index

lido_curated_staking_address = "0x55032650b14df07b85bF18A3a3eC8E0Af2e028d5"
# beacon_address = "0x00000000219ab540356cBB839Cbe05303d7705Fa"
etherscan_api_url = "https://api.etherscan.io/api"
beaconchain_api_url = "https://beaconcha.in/api/v1/validator/"

# get the number of operators
num_operators = get_number_of_operators(etherscan_api_url, lido_curated_staking_address, API_KEY)

#get total number of validators
total_deposited_validators = 0
for i in range(num_operators):
    operator_data = get_node_operator(etherscan_api_url, lido_curated_staking_address, API_KEY, i)
    deposited_validators = operator_data[6]
    total_deposited_validators += deposited_validators
    print ("total_deposited_validators: " + str(total_deposited_validators))

print ("total_deposited_validators: " + str(total_deposited_validators))

# get the  node operators' validators' deposit signatures
list_of_validators = []
for i in range(num_operators):
    operator_data = get_node_operator(etherscan_api_url, lido_curated_staking_address, API_KEY, i)
    total_deposited_validators = operator_data[6]
    for j in range(total_deposited_validators):
        deposit_signature, key, _index = get_signing_key(etherscan_api_url, lido_curated_staking_address, API_KEY, i, j)
        print ("get_signing_keys for node operator " + str(i) + " out of " + str(num_operators) +  "\nvalidator " + str(j) + " out of " + str(total_deposited_validators) + ": ")
        print ("key: " + str(key))
        index = get_index(beaconchain_api_url, key)
        print ("eth validator index: " + str(index))
        list_of_validators = {
            'node_operator_id': i,
            'validator_index': j,
            'deposit_signature': "0x" + deposit_signature,
            'key': key,
            'index': index
        }

print ("list_of_validators: " + str(list_of_validators))

    

