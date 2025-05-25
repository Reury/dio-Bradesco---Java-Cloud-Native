import os
import mimetypes
from typing import Dict, Any, List, Optional, Union
import json
import logging

logger = logging.getLogger(__name__)

class DocumentValidator:
    """Validate documents before processing"""
    
    def __init__(self, max_file_size_mb: int = 16, 
                 supported_formats: Optional[List[str]] = None):
        self.max_file_size_bytes = max_file_size_mb * 1024 * 1024
        self.supported_formats = supported_formats or [
            'pdf', 'docx', 'doc', 'txt', 'json', 'csv', 'xlsx', 'pptx'
        ]
    
    def validate_document(self, file_path: str) -> Dict[str, Any]:
        """Comprehensive document validation"""
        errors = []
        warnings = []
        
        # Check if file exists
        if not os.path.exists(file_path):
            errors.append(f"File does not exist: {file_path}")
            return {
                'is_valid': False,
                'errors': errors,
                'warnings': warnings,
                'file_path': file_path
            }
        
        # Check file size
        file_size = os.path.getsize(file_path)
        if file_size > self.max_file_size_bytes:
            errors.append(
                f"File size ({file_size / 1024 / 1024:.1f} MB) exceeds "
                f"maximum allowed size ({self.max_file_size_bytes / 1024 / 1024} MB)"
            )
        
        if file_size == 0:
            errors.append("File is empty")
        
        # Check file format
        file_ext = os.path.splitext(file_path)[1].lower().lstrip('.')
        if file_ext not in self.supported_formats:
            errors.append(
                f"Unsupported file format: .{file_ext}. "
                f"Supported formats: {', '.join(self.supported_formats)}"
            )
        
        # Check file permissions
        if not os.access(file_path, os.R_OK):
            errors.append("File is not readable")
        
        # MIME type validation
        mime_type, _ = mimetypes.guess_type(file_path)
        if not mime_type:
            warnings.append("Could not determine MIME type")
        
        # Content validation based on file type
        if file_ext == 'json':
            json_errors = self._validate_json_file(file_path)
            errors.extend(json_errors)
        elif file_ext == 'csv':
            csv_errors = self._validate_csv_file(file_path)
            errors.extend(csv_errors)
        
        return {
            'is_valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings,
            'file_path': file_path,
            'file_size': file_size,
            'file_format': file_ext,
            'mime_type': mime_type
        }
    
    def _validate_json_file(self, file_path: str) -> List[str]:
        """Validate JSON file structure"""
        errors = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                json.load(f)
        except json.JSONDecodeError as e:
            errors.append(f"Invalid JSON format: {str(e)}")
        except UnicodeDecodeError as e:
            errors.append(f"Text encoding error: {str(e)}")
        except Exception as e:
            errors.append(f"Error reading JSON file: {str(e)}")
        
        return errors
    
    def _validate_csv_file(self, file_path: str) -> List[str]:
        """Validate CSV file structure"""
        errors = []
        
        try:
            import csv
            with open(file_path, 'r', encoding='utf-8') as f:
                # Try to detect dialect
                sample = f.read(1024)
                f.seek(0)
                
                try:
                    dialect = csv.Sniffer().sniff(sample)
                except csv.Error:
                    # Use default dialect
                    dialect = csv.excel
                
                reader = csv.reader(f, dialect)
                row_count = 0
                for row in reader:
                    row_count += 1
                    if row_count > 100:  # Check first 100 rows
                        break
                
                if row_count == 0:
                    errors.append("CSV file appears to be empty")
                    
        except UnicodeDecodeError as e:
            errors.append(f"Text encoding error in CSV: {str(e)}")
        except Exception as e:
            errors.append(f"Error reading CSV file: {str(e)}")
        
        return errors

class SearchQueryValidator:
    """Validate search queries"""
    
    def __init__(self):
        self.max_query_length = 1000
        self.reserved_words = ['and', 'or', 'not']
    
    def validate_query(self, query: str) -> Dict[str, Any]:
        """Validate search query"""
        errors = []
        warnings = []
        
        if not query or not query.strip():
            errors.append("Query cannot be empty")
            return {
                'is_valid': False,
                'errors': errors,
                'warnings': warnings,
                'query': query
            }
        
        # Check query length
        if len(query) > self.max_query_length:
            errors.append(f"Query length exceeds maximum of {self.max_query_length} characters")
        
        # Check for malformed quotes
        if query.count('"') % 2 != 0:
            errors.append("Unmatched quotes in query")
        
        # Check for empty phrase searches
        if '""' in query:
            warnings.append("Empty phrase search detected")
        
        # Check for potential injection attempts
        suspicious_patterns = ['<script', 'javascript:', 'eval(', 'document.']
        for pattern in suspicious_patterns:
            if pattern.lower() in query.lower():
                errors.append("Potentially malicious content detected in query")
                break
        
        return {
            'is_valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings,
            'query': query,
            'query_length': len(query)
        }

class IndexSchemaValidator:
    """Validate index schema configurations"""
    
    def __init__(self):
        self.valid_field_types = [
            'Edm.String', 'Edm.Int32', 'Edm.Int64', 'Edm.Double',
            'Edm.Boolean', 'Edm.DateTimeOffset', 'Edm.GeographyPoint',
            'Collection(Edm.String)'
        ]
    
    def validate_schema(self, schema_fields: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Validate index schema"""
        errors = []
        warnings = []
        
        if not schema_fields:
            errors.append("Schema must contain at least one field")
            return {
                'is_valid': False,
                'errors': errors,
                'warnings': warnings
            }
        
        # Check for key field
        key_fields = [f for f in schema_fields if f.get('key', False)]
        if len(key_fields) != 1:
            errors.append("Schema must have exactly one key field")
        
        # Check field names and types
        field_names = set()
        for field in schema_fields:
            name = field.get('name', '')
            field_type = field.get('type', '')
            
            if not name:
                errors.append("Field name cannot be empty")
                continue
            
            if name in field_names:
                errors.append(f"Duplicate field name: {name}")
            field_names.add(name)
            
            # Validate field name format
            if not name.replace('_', '').replace('-', '').isalnum():
                warnings.append(f"Field name '{name}' contains special characters")
            
            # Validate field type
            if field_type not in self.valid_field_types:
                errors.append(f"Invalid field type '{field_type}' for field '{name}'")
            
            # Check searchable configuration
            if field.get('searchable', False) and field_type != 'Edm.String':
                warnings.append(f"Non-string field '{name}' marked as searchable")
        
        return {
            'is_valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings,
            'field_count': len(schema_fields),
            'key_fields': len(key_fields)
        }

class ConfigValidator:
    """Validate configuration settings"""
    
    def validate_azure_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Validate Azure configuration"""
        errors = []
        warnings = []
        
        required_fields = [
            'search_service_name',
            'search_admin_key',
            'storage_connection_string'
        ]
        
        for field in required_fields:
            if not config.get(field):
                errors.append(f"Required field '{field}' is missing or empty")
        
        # Validate search service name format
        service_name = config.get('search_service_name', '')
        if service_name and not service_name.replace('-', '').isalnum():
            warnings.append("Search service name should contain only alphanumeric characters and hyphens")
        
        # Validate connection string format
        conn_str = config.get('storage_connection_string', '')
        if conn_str and 'AccountName=' not in conn_str:
            errors.append("Invalid storage connection string format")
        
        return {
            'is_valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings,
            'config': config
        }

def validate_batch_operation(items: List[Any], max_batch_size: int = 100) -> Dict[str, Any]:
    """Validate batch operation parameters"""
    errors = []
    warnings = []
    
    if not items:
        errors.append("Batch cannot be empty")
    elif len(items) > max_batch_size:
        errors.append(f"Batch size ({len(items)}) exceeds maximum ({max_batch_size})")
    
    if len(items) > max_batch_size * 0.8:
        warnings.append("Large batch size may impact performance")
    
    return {
        'is_valid': len(errors) == 0,
        'errors': errors,
        'warnings': warnings,
        'batch_size': len(items),
        'max_batch_size': max_batch_size
    }