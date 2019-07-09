# File to be executed in Azure Cloud Shell for best performance
# First execute "pip install --user azure-cosmos" in the terminal
# This file creates the cosmos database and containers and add items to each container
# It imports the config.py file create in generateConfig.py file for getting all the credentials of the cosmos account

from azure.cosmos import cosmos_client
import os, json, time
from config import cosmos_acc_endpoint, cosmos_acc_key, database_name, file_share_directory

# Creating a cosmos client 
client = cosmos_client.CosmosClient(url_connection=cosmos_acc_endpoint, auth={'masterKey': cosmos_acc_key})

# Creating the database
db = client.CreateDatabase({'id': database_name})['_self']
throughput = 1000

# Change directory to folder which has all the ndjson files
os.chdir(file_share_directory)
for file_name in os.listdir():
    if not file_name.endswith('.ndjson'): continue
    container_name = file_name.split('.')[0]
    print('Creating container', container_name, 'with {}'.format(throughput), 'RU/s')
    container = client.CreateContainer(db, {'id': container_name}, options={'offerThroughput': throughput})['_self']
    line_count = 0
    t = time.time()
    with open(file_name) as f:
        for line in f:
            line_count += 1
            client.CreateItem(container, json.loads(line))
    print(file_name, 'has', line_count, 'records and took', time.time() - t, 'seconds to get uploaded into cosmos')
    # Getting the throughput properties of the container
    offer = list(client.QueryOffers('select * from c where c.resource = "{}"'.format(container)))[0]
    # Changing to base value 400
    offer['content']['offerThroughput'] = 400
    print('Reverting back to 400 RU/s')
    client.ReplaceOffer(offer['_self'], offer)
