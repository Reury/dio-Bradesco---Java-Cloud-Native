import os
import asyncio
from typing import List, Dict, Any, Optional
from azure.storage.blob.aio import BlobServiceClient
from azure.core.exceptions import ResourceExistsError
import logging

logger = logging.getLogger(__name__)

class AsyncBlobUploader:
    """Asynchronous blob uploader for better performance"""
    
    def __init__(self, connection_string: str, container_name: str):
        self.connection_string = connection_string
        self.container_name = container_name
    
    async def upload_files_async(self, file_paths: List[str], 
                                max_concurrent: int = 5) -> List[Dict[str, Any]]:
        """Upload multiple files asynchronously"""
        async with BlobServiceClient.from_connection_string(
            self.connection_string
        ) as blob_service_client:
            
            await self._ensure_container_exists(blob_service_client)
            
            semaphore = asyncio.Semaphore(max_concurrent)
            tasks = [
                self._upload_single_file(blob_service_client, file_path, semaphore)
                for file_path in file_paths
            ]
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Handle exceptions
            processed_results = []
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    processed_results.append({
                        'success': False,
                        'file_path': file_paths[i],
                        'error': str(result)
                    })
                else:
                    processed_results.append(result)
            
            return processed_results
    
    async def _ensure_container_exists(self, blob_service_client) -> None:
        """Ensure container exists"""
        try:
            container_client = blob_service_client.get_container_client(
                self.container_name
            )
            await container_client.create_container()
            logger.info(f"Created container: {self.container_name}")
        except ResourceExistsError:
            logger.info(f"Container {self.container_name} already exists")
    
    async def _upload_single_file(self, blob_service_client, 
                                 file_path: str, semaphore) -> Dict[str, Any]:
        """Upload a single file with semaphore control"""
        async with semaphore:
            try:
                blob_name = os.path.basename(file_path)
                blob_client = blob_service_client.get_blob_client(
                    container=self.container_name,
                    blob=blob_name
                )
                
                with open(file_path, 'rb') as data:
                    await blob_client.upload_blob(data, overwrite=True)
                
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

class BlobUploader:
    """Synchronous wrapper for the async uploader"""
    
    def __init__(self, connection_string: str, container_name: str):
        self.async_uploader = AsyncBlobUploader(connection_string, container_name)
    
    def upload_files(self, file_paths: List[str], 
                    max_concurrent: int = 5) -> List[Dict[str, Any]]:
        """Upload files synchronously"""
        return asyncio.run(
            self.async_uploader.upload_files_async(file_paths, max_concurrent)
        )