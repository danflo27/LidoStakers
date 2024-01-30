- gets number of lido node operators via etherscan 
- gets number of deposited validators per operator via etherscan
- gets each deposited validators' pubKey via etherscan
- uses pubkey to get eth validator index via beaconcha.in api 

To do:
- handle api rate limits (maybe use etherscan instead of beaconcha.in)
- generate .csv from list


