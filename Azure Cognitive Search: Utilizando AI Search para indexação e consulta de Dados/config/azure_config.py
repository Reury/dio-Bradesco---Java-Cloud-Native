import os
from typing import Dict, Optional
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

# Load environment variables
load_dotenv()

class AzureConfig:
    """Azure configuration management class"""
    
    def __init__(self):
        self.search_service_name = os.getenv('AZURE_SEARCH_SERVICE_NAME')
        self.search_admin_key = os.getenv('AZURE_SEARCH_ADMIN_KEY')
        self.search_query_key = os.getenv('AZURE_SEARCH_QUERY_KEY')
        self.search_index_name = os.getenv('AZURE_SEARCH_INDEX_NAME', 'documents-index')
        
        self.storage_connection_string = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
        self.storage_container_name = os.getenv('AZURE_STORAGE_CONTAINER_NAME', 'documents')
        
        self.cognitive_services_key = os.getenv('COGNITIVE_SERVICES_KEY')
        self.cognitive_services_endpoint = os.getenv('COGNITIVE_SERVICES_ENDPOINT')
        
        self.form_recognizer_endpoint = os.getenv('FORM_RECOGNIZER_ENDPOINT')
        self.form_recognizer_key = os.getenv('FORM_RECOGNIZER_KEY')
        
        self.key_vault_url = os.getenv('KEY_VAULT_URL')
        
    def get_search_endpoint(self) -> str:
        """Get the search service endpoint URL"""
        return f"https://{self.search_service_name}.search.windows.net"
    
    def validate_config(self) -> Dict[str, bool]:
        """Validate required configuration values"""
        validations = {
            'search_service_name': bool(self.search_service_name),
            'search_admin_key': bool(self.search_admin_key),
            'storage_connection_string': bool(self.storage_connection_string),
            'cognitive_services_key': bool(self.cognitive_services_key)
        }
        return validations
    
    def get_secret_from_keyvault(self, secret_name: str) -> Optional[str]:
        """Retrieve secret from Azure Key Vault"""
        if not self.key_vault_url:
            return None
            
        try:
            credential = DefaultAzureCredential()
            client = SecretClient(vault_url=self.key_vault_url, credential=credential)
            secret = client.get_secret(secret_name)
            return secret.value
        except Exception as e:
            print(f"Error retrieving secret {secret_name}: {e}")
            return None

# Global configuration instance
config = AzureConfig()