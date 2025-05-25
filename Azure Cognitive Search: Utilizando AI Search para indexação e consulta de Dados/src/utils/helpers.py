import os
import mimetypes
import hashlib
from typing import Dict, Any, Optional, List
from datetime import datetime
import json
import logging

logger = logging.getLogger(__name__)

def get_file_metadata(file_path: str) -> Dict[str, Any]:
    """Extract metadata from a file"""
    try:
        stat = os.stat(file_path)
        mime_type, _ = mimetypes.guess_type(file_path)
        
        metadata = {
            'filename': os.path.basename(file_path),
            'file_size': stat.st_size,
            'file_type': get_file_extension(file_path),
            'mime_type': mime_type or 'application/octet-stream',
            'created_date': datetime.fromtimestamp(stat.st_ctime).isoformat(),
            'modified_date': datetime.fromtimestamp(stat.st_mtime).isoformat(),
            'file_hash': calculate_file_hash(file_path)
        }
        
        return metadata
        
    except Exception as e:
        logger.error(f"Error extracting metadata from {file_path}: {e}")
        return {
            'filename': os.path.basename(file_path),
            'error': str(e)
        }

def get_file_extension(file_path: str) -> str:
    """Get file extension in lowercase"""
    return os.path.splitext(file_path)[1].lower().lstrip('.')

def validate_file_format(file_path: str, 
                        supported_formats: Optional[List[str]] = None) -> bool:
    """Validate if file format is supported"""
    if supported_formats is None:
        supported_formats = ['pdf', 'docx', 'doc', 'txt', 'json', 'csv', 'xlsx']
    
    file_ext = get_file_extension(file_path)
    return file_ext in supported_formats

def calculate_file_hash(file_path: str, algorithm: str = 'md5') -> str:
    """Calculate file hash for deduplication"""
    try:
        hash_algo = hashlib.new(algorithm)
        
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_algo.update(chunk)
        
        return hash_algo.hexdigest()
        
    except Exception as e:
        logger.error(f"Error calculating hash for {file_path}: {e}")
        return ""

def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe storage"""
    # Remove or replace invalid characters
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    
    # Limit length
    if len(filename) > 255:
        name, ext = os.path.splitext(filename)
        filename = name[:255-len(ext)] + ext
    
    return filename

def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} PB"

def extract_text_preview(content: str, max_length: int = 200) -> str:
    """Extract a preview of text content"""
    if not content:
        return ""
    
    # Clean up the content
    cleaned = ' '.join(content.split())
    
    if len(cleaned) <= max_length:
        return cleaned
    
    # Find a good breaking point (end of sentence or word)
    preview = cleaned[:max_length]
    
    # Try to break at sentence end
    last_period = preview.rfind('.')
    if last_period > max_length * 0.7:  # At least 70% of desired length
        return preview[:last_period + 1]
    
    # Break at word boundary
    last_space = preview.rfind(' ')
    if last_space > 0:
        return preview[:last_space] + "..."
    
    return preview + "..."

def parse_date_string(date_str: str) -> Optional[datetime]:
    """Parse various date string formats"""
    if not date_str:
        return None
    
    formats = [
        '%Y-%m-%d',
        '%Y-%m-%dT%H:%M:%S',
        '%Y-%m-%dT%H:%M:%S.%f',
        '%Y-%m-%dT%H:%M:%SZ',
        '%Y-%m-%dT%H:%M:%S.%fZ',
        '%d/%m/%Y',
        '%m/%d/%Y',
        '%Y/%m/%d'
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    
    logger.warning(f"Could not parse date string: {date_str}")
    return None

def clean_text(text: str) -> str:
    """Clean and normalize text content"""
    if not text:
        return ""
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    # Remove control characters
    text = ''.join(char for char in text if ord(char) >= 32 or char in '\n\t')
    
    return text.strip()

def chunk_text(text: str, chunk_size: int = 4000, overlap: int = 200) -> List[str]:
    """Split text into overlapping chunks"""
    if len(text) <= chunk_size:
        return [text]
    
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + chunk_size
        
        if end >= len(text):
            chunks.append(text[start:])
            break
        
        # Find a good breaking point
        break_point = text.rfind(' ', start, end)
        if break_point == -1 or break_point <= start:
            break_point = end
        
        chunks.append(text[start:break_point])
        start = break_point - overlap
        
        if start < 0:
            start = 0
    
    return chunks

def merge_dictionaries(*dicts: Dict[str, Any]) -> Dict[str, Any]:
    """Merge multiple dictionaries with conflict resolution"""
    result = {}
    
    for d in dicts:
        for key, value in d.items():
            if key in result:
                # Handle conflicts
                if isinstance(result[key], list) and isinstance(value, list):
                    result[key].extend(value)
                elif isinstance(result[key], dict) and isinstance(value, dict):
                    result[key] = merge_dictionaries(result[key], value)
                else:
                    # Overwrite with latest value
                    result[key] = value
            else:
                result[key] = value
    
    return result

def safe_json_loads(json_str: str, default: Any = None) -> Any:
    """Safely parse JSON string with fallback"""
    try:
        return json.loads(json_str)
    except (json.JSONDecodeError, TypeError):
        return default

def create_directory_if_not_exists(directory: str) -> bool:
    """Create directory if it doesn't exist"""
    try:
        os.makedirs(directory, exist_ok=True)
        return True
    except Exception as e:
        logger.error(f"Error creating directory {directory}: {e}")
        return False

def get_environment_variable(var_name: str, default: Any = None, 
                           required: bool = False) -> Any:
    """Get environment variable with validation"""
    value = os.getenv(var_name, default)
    
    if required and value is None:
        raise ValueError(f"Required environment variable {var_name} is not set")
    
    return value

def setup_logging(log_level: str = "INFO", log_file: Optional[str] = None) -> None:
    """Setup logging configuration"""
    level = getattr(logging, log_level.upper(), logging.INFO)
    
    handlers = [logging.StreamHandler()]
    
    if log_file:
        # Create log directory if needed
        log_dir = os.path.dirname(log_file)
        if log_dir:
            create_directory_if_not_exists(log_dir)
        handlers.append(logging.FileHandler(log_file))
    
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=handlers
    )

def validate_azure_connection_string(connection_string: str) -> bool:
    """Validate Azure storage connection string format"""
    required_parts = ['AccountName=', 'AccountKey=', 'EndpointSuffix=']
    return all(part in connection_string for part in required_parts)

def extract_entities_from_text(text: str, entity_types: List[str]) -> Dict[str, List[str]]:
    """Simple entity extraction (placeholder for more sophisticated NLP)"""
    # This is a simple implementation - in production, use Azure Cognitive Services
    import re
    
    entities = {entity_type: [] for entity_type in entity_types}
    
    if 'email' in entity_types:
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        entities['email'] = re.findall(email_pattern, text)
    
    if 'url' in entity_types:
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        entities['url'] = re.findall(url_pattern, text)
    
    if 'phone' in entity_types:
        phone_pattern = r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'
        entities['phone'] = re.findall(phone_pattern, text)
    
    return entities