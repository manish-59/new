# File to create Cosmos and Storage Accounts

# This file reads the required parameters(like the name, location etc.) for creating storage and CosmosDB account 
# from the json files present in the templates folder and creates all the resources using azure-cli commands

# To run azure-cli commands in our script, subprocess module is used

import json, subprocess, sys

# Uncomment the below lines if you have your azure CLI logged in
# cmd = ['az', 'login']
# subprocess.getstatusoutput(cmd)

# Get the first resource group name from the returned list of resource groups
print('Querying for resource group')
cmd = 'az group list --query [0].name -o tsv'
cmd = cmd.split()
# Run the cmd and remove the extra quotations
res_gp = subprocess.getoutput(cmd)
print(res_gp, 'found!')

# Reading storage parameters from storageParameters.json file in templates/ directory
print('Reading from storagePararmeters.json')
with open('templates/storageParameters.json') as f:
    storage_parameters = json.load(f)
storage_acc_name = storage_parameters['parameters']['storageAccountName']['value']

# Checking if the storage account already exists
print('Let\'s see if you have the storage account')
cmd = 'az storage account list --query [].name -o tsv'
storage_accounts = subprocess.getoutput(cmd).split()
already_exists = (storage_acc_name in storage_accounts)

# If the storage account doesn't exist, create one
if not already_exists:
    cmd = 'az storage account check-name -n {} --query nameAvailable'.format(storage_acc_name)
    name_available = subprocess.getoutput(cmd)
    name_available = (name_available == 'true')
    while not name_available:
        print('Sorry the storage account name is taken. Choose another name and try again')
        storage_acc_name = input('Enter a new name: ')
        cmd = 'az storage account check-name -n {} --query nameAvailable'.format(storage_acc_name)
        name_available = subprocess.getoutput(cmd)
        name_available = (name_available == 'true')
        if name_available:
            storage_parameters['parameters']['storageAccountName']['value'] = storage_acc_name
            print('Available! Writing to storageParameters.json')
            with open('templates/storageParameters.json', 'w') as f:
                json.dump(storage_parameters, f, indent=4)

    print('Creating..')
    cmd = 'az group deployment create -g {} \
--template-file templates/storageTemplate.json \
--parameters @templates/storageParameters.json'.format(res_gp)
    
    
    subprocess.getstatusoutput(cmd)
    print('Storage account', storage_acc_name, 'has been created successfully!')
else:
    print('You already have the storage account!')

# Reading cosmos parameters from cosmosParameters.json file in templates/ directory
print('Reading from cosmosPararmeters.json')
with open('templates/cosmosParameters.json') as f:
    cosmos_parameters = json.load(f)
cosmos_acc_name = cosmos_parameters['parameters']['name']['value']

# Checking if the CosmosDB account already exists
print('Let\'s see if you have the cosmos account')
cmd = 'az cosmosdb list --query [].name -o tsv'
cmd = cmd.split()
cosmos_accounts = subprocess.getoutput(cmd).split()
already_exists = (cosmos_acc_name in cosmos_accounts)

if not already_exists:
    cmd = 'az cosmosdb check-name-exists -n {}'.format(cosmos_acc_name)
    cmd = cmd.split()
    name_available = subprocess.getoutput(cmd)
    while not name_available:
        print('Sorry the cosmos account name is taken. Choose another name')
        cosmos_acc_name = input('Enter a new name: ')
        cmd = 'az cosmosdb check-name-exists -n {}'.format(cosmos_acc_name)
        cmd = cmd.split()
        name_available = subprocess.getoutput(cmd)
        name_available = (name_available == 'true')
        if name_available:
            cosmos_parameters['parameters']['name']['value'] = cosmos_acc_name
            print('Available! Writing to cosmosParameters.json')
            with open('templates/cosmosParameters.json', 'w') as f:
                json.dump(cosmos_parameters, f, indent=4)
    print('Creating..')
    cmd = ['az', 'group', 'deployment', 'create', '-g', res_gp,\
        '--template-file', 'templates/cosmosTemplate.json',\
            '--parameters', '@templates/cosmosParameters.json']
    subprocess.getstatusoutput(cmd)
    print('CosmosDB account', cosmos_acc_name, 'has been created successfully!')
else:
    print('You already have the cosmos account!')
