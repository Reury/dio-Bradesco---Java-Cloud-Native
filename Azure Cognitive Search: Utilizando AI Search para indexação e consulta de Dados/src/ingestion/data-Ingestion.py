import os
import logging
from typing import List, Dict, Any, Optional
from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import ResourceExistsError
from ..utils.helpers import get_file_metadata, validate_file_format
from ..utils.validators import DocumentValidator

logger = logging.getLogger(__name__)

class DocumentIngestion:
    """Handle document ingestion to Azure Blob Storage"""
    
    def __init__(self, storage_connection_string: str, container_name: str):
        self.blob_service_client = BlobServiceClient.from_connection_string(storage_connection_string)
        self.container_name = container_name
        self.validator = DocumentValidator()
        self._ensure_container_exists()
    
    def _ensure_container_exists(self) -> None:
        """Create container if it doesn't exist"""
        try:
            container_client = self.blob_service_client.get_container_client(self.container_name)
            container_client.create_container()
            logger.info(f"Created container: {self.container_name}")
        except ResourceExistsError:
            logger.info(f"Container {self.container_name} already exists")
    
    def upload_document(self, file_path: str, blob_name: Optional[str] = None) -> Dict[str, Any]:
        """Upload a single document to blob storage"""
        if not blob_name:
            blob_name = os.path.basename(file_path)
        
        # Validate document
        validation_result = self.validator.validate_document(file_path)
        if not validation_result['is_valid']:
            return {
                'success': False,
                'file_path': file_path,
                'error': validation_result['errors']
            }
        
        try:
            blob_client = self.blob_service_client.get_blob_client(
                container=self.container_name, 
                blob=blob_name
            )
            
            with open(file_path, 'rb') as data:
                metadata = get_file_metadata(file_path)
                blob_client.upload_blob(data, metadata=metadata, overwrite=True)
            
            logger.info(f"Successfully uploaded: {blob_name}")
            return {
                'success': True,
                'file_path': file_path,
                'blob_name': blob_name,
                'url': blob_client.url
            }
            
        except Exception as e:
            logger.error(f"Error uploading {file_path}: {e}")
            return {
                'success': False,
                'file_path': file_path,
                'error': str(e)
            }
    
    def process_documents_batch(self, directory_path: str) -> List[Dict[str, Any]]:
        """Process multiple documents from a directory"""
        results = []
        
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                file_path = os.path.join(root, file)
                if validate_file_format(file_path):
                    result = self.upload_document(file_path)
                    results.append(result)
                else:
                    logger.warning(f"Skipping unsupported file: {file_path}")
        
        return results
    
    def get_ingestion_stats(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate statistics from ingestion results"""
        total_files = len(results)
        successful = sum(1 for r in results if r['success'])
        failed = total_files - successful
        
        return {
            'total_files': total_files,
            'successful': successful,
            'failed': failed,
            'success_rate': (successful / total_files * 100) if total_files > 0 else 0
        }