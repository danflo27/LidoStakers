import requests
from config import API_KEY

# Define the API endpoint
api_url = "https://api.etherscan.io/api" # 5 calls per sec, 100k calls per day

continue_loop = True
start_block = 11480180 # first block involving Lido

params = {
    'module': 'proxy',
    'action': 'eth_blockNumber',
    'apikey': API_KEY
}

response = requests.get(api_url, params=params)
data = response.json()
newest_block = int(data['result'], 16)

while continue_loop:
    # Define the parameters
    params = {
        'module': 'account',
        'action': 'txlist',
        'address': '0xae7ab96520DE3A18E5e111B5EaAb095312D7fE84',
        'startblock': start_block, 
        'endblock': 'latest', 
        'apikey': API_KEY  
    }

    # Make the API call
    response = requests.get(api_url, params=params)

    # Check the response
    if response.status_code == 200:
        data = response.json()
        print(data)
    else:
        print(f"Error: {response.status_code} - {response.text}")

    lastBlock = None
    firstBlock = None
    list = []
    for i in data['result']:
        m = i["methodId"]
        a = i["from"]
        firstBlock = data['result'][0]["blockNumber"]
        b = i["blockNumber"]
        # print (blocknum, m, a)
        if m == "0xa1903eab": # submit methodID
            list.append([m, a, b]) # methodID, address, blockNumber
        lastBlock = int(b)

    step = lastBlock - int(firstBlock)
    start_block = lastBlock + step

    print (list)
    print ("first block in loop: " + str(firstBlock))
    print ("last block in loop: " + str(lastBlock))
    print ("loop range: " + str(step))
    print ("number of tx found: " + str(len(list))) 
    print ("starting next loop at " + str(start_block))
    print ("searching until block: " + str(newest_block))

    if int(start_block) > newest_block:
        continue_loop = False
    else:
        continue_loop = True

    params = {
        'module': 'account',
        'action': 'txlist',
        'address': '0xae7ab96520DE3A18E5e111B5EaAb095312D7fE84',
        'startblock': start_block, # first block involving Lido
        'endblock': 'latest', 
        'apikey': API_KEY  
    }



