from findOperators import get_node_operator, get_number_of_operators, contract_address, API_KEY, api_url

# get the number of operators
numOperators = get_number_of_operators(api_url, contract_address, API_KEY)

# get the operator data
for i in range(numOperators):
    get_node_operator(api_url, contract_address, API_KEY, i)
    
