# This file generates a config.py file which contains all the credentials of the azure account like the primary keys, URL endoints of 
# storage and CosmosDB accounts and also stores the file share name and directory

# It first imports the createResources.py file which creates all the resources before the generation of the config.py file

from createResources import storage_acc_name, cosmos_acc_name, res_gp
import subprocess, shutil

database_name = 'synthea'
file_share_name = 'syntheafs'
file_share_directory = 'r4-small'

print('Creating config.py to store all credentials')
# Creating new file or overwriting already existing file
with open('config.py', 'w') as f:
    # Writing storage account name
    f.write('storage_acc_name = \'{}\'\n'.format(storage_acc_name))
    # Writing cosmos account name
    f.write('cosmos_acc_name = \'{}\'\n'.format(cosmos_acc_name))
    # Writing database name that needs to be created in cosmos
    f.write('database_name = \'{}\'\n'.format(database_name))
    # Writing file share name name that needs to be created in storage account
    f.write('file_share_name = \'{}\'\n'.format(file_share_name))
    # Writing directory name that needs to be created in file share
    f.write('file_share_directory = \'{}\'\n'.format(file_share_directory))
    # Getting storage account keys
    cmd = ['az', 'storage', 'account', 'keys', 'list', '-n', storage_acc_name, '--query', '[0].value']
    storage_acc_key = subprocess.getoutput(cmd)[1:-1]
    f.write('storage_acc_key = \'{}\'\n'.format(storage_acc_key))
    # Getting cosmos account keys
    cmd = ['az', 'cosmosdb', 'keys', 'list', '-n', cosmos_acc_name, '-g', res_gp, '--query', 'primaryMasterKey']
    cosmos_acc_key = subprocess.getoutput(cmd)[1:-1]
    f.write('cosmos_acc_key = \'{}\'\n'.format(cosmos_acc_key))
    # Getting cosmos account endpoint URL
    cmd = ['az', 'cosmosdb', 'show', '-n', cosmos_acc_name, '-g', res_gp, '--query', 'documentEndpoint']
    cosmos_acc_endpoint = subprocess.getoutput(cmd)[1:-1]
    f.write('cosmos_acc_endpoint = \'{}\'\n'.format(cosmos_acc_endpoint))

print('Finished writing to config.py')

# Copy the same config.py file into Flask directory
shutil.copyfile('config.py', '../Flask/config.py')
