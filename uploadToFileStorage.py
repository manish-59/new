# To run this file execute the following commmand in the terminal "pip install --user azure-storage"
# This is the only file to be executed on the local system

from azure.storage.file import FileService
import os, generateConfig, subprocess
from config import file_share_name, storage_acc_name, storage_acc_key, file_share_directory

try:
    file_service = FileService(account_name=storage_acc_name, account_key=storage_acc_key)

    # Creating the file share in Storage account
    print('Creating file share')
    file_service.create_share(file_share_name, quota=6)
    # Creating a directory in file share
    print('Creating', file_share_directory, 'directory')
    file_service.create_directory(file_share_name, file_share_directory)

    # Uploading the ndjson2cosmos.py and the generated config.py file to file share
    file_name = 'ndjson2cosmos.py'
    print('Uploading', file_name, 'to file service')
    file_service.create_file_from_path(file_share_name, None, file_name, file_name)
    print('Done')
    file_name = 'config.py'
    print('Uploading', file_name, 'to file service')
    file_service.create_file_from_path(file_share_name, None, file_name, file_name)
    print('Done')

    # Uploading all the ndjson files to file share
    os.chdir('r4-small')
    for file_name in os.listdir():
        print('Uploading', file_name, 'to file service into', file_share_directory, 'directory')
        file_service.create_file_from_path(file_share_name, file_share_directory, file_name, file_name)
        print('Done')

except:
    # The above method may fail on UHG network due to limitation of port 443
    # You will get an SSL error
    # To avoid that, you can install AzCopy and use that command to upload files
    # Drawback of this method is it allocates 5TB storage quota in the file share
    # You'll have to manually change the quota in Azure Portal

    print('Sorry there was an error. Trying a different method')
    print('Uploading ndjson files into', file_share_directory, 'directory located in', file_share_name, 'file share')
    cmd = 'azcopy /Source:r4-small \
/Dest:https://{}.file.core.windows.net/{}/{} \
/DestKey:{} /Y'.format(storage_acc_name, file_share_name, file_share_directory, storage_acc_key).split()
    # print(subprocess.getoutput(cmd))
    print('Done!')
    for file_name in ('ndjson2cosmos.py', 'config.py'):
        print('Uploading {} into file share'.format(file_name))
        cmd = 'azcopy /Source:{} \
    /Dest:https://{}.file.core.windows.net/{}/{} \
    /DestKey:{} /Y'.format(file_name, storage_acc_name, file_share_name, file_name, storage_acc_key)
        subprocess.getstatusoutput(cmd)
        print('Done!')
