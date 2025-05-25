from typing import Dict, Any, List, Optional
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex, SimpleField, SearchableField, SearchFieldDataType,
    ComplexField, CorsOptions
)
from azure.core.credentials import AzureKeyCredential
import logging

logger = logging.getLogger(__name__)

class IndexManager:
    """Manage Azure Cognitive Search indexes"""
    
    def __init__(self, service_name: str, admin_key: str):
        self.service_endpoint = f"https://{service_name}.search.windows.net"
        self.admin_client = SearchIndexClient(
            endpoint=self.service_endpoint,
            credential=AzureKeyCredential(admin_key)
        )
    
    def create_index(self, index_name: str, fields: List[Any]) -> Dict[str, Any]:
        """Create a new search index"""
        try:
            # Configure CORS
            cors_options = CorsOptions(
                allowed_origins=["*"],
                max_age_in_seconds=300
            )
            
            index = SearchIndex(
                name=index_name,
                fields=fields,
                cors_options=cors_options
            )
            
            result = self.admin_client.create_index(index)
            logger.info(f"Created index: {index_name}")
            
            return {
                'success': True,
                'index_name': index_name,
                'field_count': len(fields)
            }
            
        except Exception as e:
            logger.error(f"Error creating index {index_name}: {e}")
            return {
                'success': False,
                'index_name': index_name,
                'error': str(e)
            }
    
    def update_index(self, index_name: str, fields: List[Any]) -> Dict[str, Any]:
        """Update an existing index"""
        try:
            existing_index = self.admin_client.get_index(index_name)
            existing_index.fields = fields
            
            result = self.admin_client.create_or_update_index(existing_index)
            logger.info(f"Updated index: {index_name}")
            
            return {
                'success': True,
                'index_name': index_name,
                'field_count': len(fields)
            }
            
        except Exception as e:
            logger.error(f"Error updating index {index_name}: {e}")
            return {
                'success': False,
                'index_name': index_name,
                'error': str(e)
            }
    
    def delete_index(self, index_name: str) -> Dict[str, Any]:
        """Delete an index"""
        try:
            self.admin_client.delete_index(index_name)
            logger.info(f"Deleted index: {index_name}")
            
            return {
                'success': True,
                'index_name': index_name
            }
            
        except Exception as e:
            logger.error(f"Error deleting index {index_name}: {e}")
            return {
                'success': False,
                'index_name': index_name,
                'error': str(e)
            }
    
    def list_indexes(self) -> List[str]:
        """List all indexes in the service"""
        try:
            indexes = self.admin_client.list_indexes()
            return [index.name for index in indexes]
        except Exception as e:
            logger.error(f"Error listing indexes: {e}")
            return []
    
    def get_index_statistics(self, index_name: str) -> Dict[str, Any]:
        """Get statistics for an index"""
        try:
            stats = self.admin_client.get_index_statistics(index_name)
            return {
                'document_count': stats.document_count,
                'storage_size': stats.storage_size
            }
        except Exception as e:
            logger.error(f"Error getting statistics for {index_name}: {e}")
            return {}