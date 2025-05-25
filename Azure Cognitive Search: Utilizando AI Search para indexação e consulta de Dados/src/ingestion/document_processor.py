import mimetypes
from typing import Dict, Any, Optional
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
import logging

logger = logging.getLogger(__name__)

class DocumentProcessor:
    """Process different types of documents and extract content"""
    
    def __init__(self, form_recognizer_endpoint: str, form_recognizer_key: str):
        self.document_client = DocumentAnalysisClient(
            endpoint=form_recognizer_endpoint,
            credential=AzureKeyCredential(form_recognizer_key)
        )
    
    def process_document(self, file_path: str) -> Dict[str, Any]:
        """Process document and extract content based on file type"""
        mime_type, _ = mimetypes.guess_type(file_path)
        
        try:
            if mime_type == 'application/pdf':
                return self._process_pdf(file_path)
            elif mime_type in ['application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']:
                return self._process_word_document(file_path)
            elif mime_type == 'text/plain':
                return self._process_text_file(file_path)
            else:
                return self._process_generic_document(file_path)
                
        except Exception as e:
            logger.error(f"Error processing document {file_path}: {e}")
            return {
                'success': False,
                'error': str(e),
                'file_path': file_path
            }
    
    def _process_pdf(self, file_path: str) -> Dict[str, Any]:
        """Process PDF document using Form Recognizer"""
        with open(file_path, 'rb') as f:
            poller = self.document_client.begin_analyze_document(
                "prebuilt-document", f
            )
            result = poller.result()
        
        content = ""
        tables = []
        
        for page in result.pages:
            for line in page.lines:
                content += line.content + "\n"
        
        for table in result.tables:
            table_data = []
            for cell in table.cells:
                table_data.append({
                    'content': cell.content,
                    'row_index': cell.row_index,
                    'column_index': cell.column_index
                })
            tables.append(table_data)
        
        return {
            'success': True,
            'content': content,
            'tables': tables,
            'page_count': len(result.pages),
            'file_path': file_path
        }
    
    def _process_word_document(self, file_path: str) -> Dict[str, Any]:
        """Process Word document"""
        with open(file_path, 'rb') as f:
            poller = self.document_client.begin_analyze_document(
                "prebuilt-document", f
            )
            result = poller.result()
        
        content = result.content if result.content else ""
        
        return {
            'success': True,
            'content': content,
            'file_path': file_path
        }
    
    def _process_text_file(self, file_path: str) -> Dict[str, Any]:
        """Process plain text file"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return {
            'success': True,
            'content': content,
            'file_path': file_path
        }
    
    def _process_generic_document(self, file_path: str) -> Dict[str, Any]:
        """Process generic document using Form Recognizer"""
        try:
            with open(file_path, 'rb') as f:
                poller = self.document_client.begin_analyze_document(
                    "prebuilt-document", f
                )
                result = poller.result()
            
            content = result.content if result.content else ""
            
            return {
                'success': True,
                'content': content,
                'file_path': file_path
            }
        except Exception as e:
            return {
                'success': False,
                'error': f"Unable to process document type: {str(e)}",
                'file_path': file_path
            }