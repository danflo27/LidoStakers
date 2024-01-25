from validatorIndices import get_node_operator, get_number_of_operators, contract_address, API_KEY, api_url

get_number_of_operators(api_url, contract_address, API_KEY)

for i in range(39):
    get_node_operator(api_url, contract_address, API_KEY, i)
