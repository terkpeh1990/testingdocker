from storages.backends.azure_storage import AzureStorage
from django.conf import settings



class AzureMediaStorage(AzureStorage):
    account_name = settings.AZURE_ACCOUNT_NAME # Must be replaced by your <storage_account_name>
    account_key = settings.AZURE_ACCOUNT_KEY # Must be replaced by your <storage_account_key>
    azure_container = settings.MEDIA_LOCATION
    expiration_secs = None
    
# class AzureStaticStorage(AzureStorage):
#     account_name = 'djangoaccountstorage' # Must be replaced by your storage_account_name
#     account_key = 'your_key_here' # Must be replaced by your <storage_account_key>
#     azure_container = 'static'
#     expiration_secs = None