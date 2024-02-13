from curated_staking_contract import get_node_operator, get_number_of_operators, get_signing_key, API_KEY
from beacon_contract import get_indices
import csv
import time

lido_curated_staking_address = "0x55032650b14df07b85bF18A3a3eC8E0Af2e028d5"
etherscan_api_url = "https://api.etherscan.io/api" #100k API calls per day, 5 per sec 
beaconchain_api_url = "https://beaconcha.in/api/v1/validator/" # 5 calls per sec, 20 calls per min, 30k calls per month

list_of_validators = []
keys = []
key_to_operator_validator = {} 

# get the number of operators
num_operators = get_number_of_operators(etherscan_api_url, lido_curated_staking_address, API_KEY)

#get total number of validators belonging to node operators
total_deposited_validators = 0
for i in range(num_operators):
    operator_data = get_node_operator(etherscan_api_url, lido_curated_staking_address, API_KEY, i)
    deposited_validators = operator_data[6]
    total_deposited_validators += deposited_validators
    print ("total_deposited_validators: " + str(total_deposited_validators))
    print ()
print("\n" * 3)
print ("there are " + str(total_deposited_validators) + " validators to find." + "\n" *5)

start_operator = 0
start_validator = 0
# get the pub key for each validator and use that find their eth validator index
for i in range(start_operator, num_operators):
    validators_per_operator = get_node_operator(etherscan_api_url, lido_curated_staking_address, API_KEY, i)[6]
    for j in range(start_validator, validators_per_operator):
        deposit_signature, key, _index = get_signing_key(etherscan_api_url, lido_curated_staking_address, API_KEY, i, j)
        print ("validator " + str(j) + " / " + str(validators_per_operator) + "\nfor node operator " + str(i) + " / " + str(num_operators))
        print ("pubkey: " + str(key))
        print ()
        keys.append(key)
        # time.sleep(1)
        if len(keys) == 80:
            print ()
            time.sleep(8)
            keys_string = ','.join(keys)
            indices = get_indices(beaconchain_api_url, keys_string)
            for index in indices:
                key = keys[indices.index(index)]
                node_operator_id = i
                validator_index = index
                key_to_operator_validator[index] = {'node_operator_id': node_operator_id, 'validator_pubkey': key}  # store the mapping from index to node operator and pub key
                print(f'key: {key}, node_operator_id: {node_operator_id}, validator_index: {validator_index}')
            keys = []
            with open(f'operator_{i}.csv', 'w', newline='') as csvfile:       
                fieldnames = ['validator_index', 'node_operator_id', 'validator_pubkey']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                # Write the header
                writer.writeheader()

                # Write the rows
                for index, info in key_to_operator_validator.items():
                    row = {'validator_index': index, 'node_operator_id': info['node_operator_id'], 'validator_pubkey': info['validator_pubkey']}
                    writer.writerow(row)

    

