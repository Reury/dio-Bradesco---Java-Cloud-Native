from typing import Dict, Any, List, Optional, Union
from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizedQuery
from azure.core.credentials import AzureKeyCredential
import logging

logger = logging.getLogger(__name__)

class IntelligentSearch:
    """Intelligent search engine with advanced capabilities"""
    
    def __init__(self, service_name: str, query_key: str, index_name: str):
        self.service_endpoint = f"https://{service_name}.search.windows.net"
        self.search_client = SearchClient(
            endpoint=self.service_endpoint,
            index_name=index_name,
            credential=AzureKeyCredential(query_key)
        )
        self.index_name = index_name
    
    def simple_search(self, query: str, top: int = 50) -> Dict[str, Any]:
        """Perform a simple text search"""
        try:
            results = self.search_client.search(
                search_text=query,
                top=top,
                include_total_count=True
            )
            
            documents = []
            for result in results:
                doc = dict(result)
                documents.append(doc)
            
            return {
                'success': True,
                'query': query,
                'total_count': results.get_count(),
                'documents': documents,
                'facets': {}
            }
            
        except Exception as e:
            logger.error(f"Error in simple search: {e}")
            return {
                'success': False,
                'query': query,
                'error': str(e),
                'documents': [],
                'total_count': 0
            }
    
    def advanced_search(self, query: str, filters: Optional[str] = None,
                       facets: Optional[List[str]] = None, 
                       order_by: Optional[List[str]] = None,
                       top: int = 50, skip: int = 0) -> Dict[str, Any]:
        """Perform advanced search with filters and facets"""
        try:
            search_params = {
                'search_text': query,
                'filter': filters,
                'order_by': order_by,
                'top': top,
                'skip': skip,
                'include_total_count': True,
                'highlight_fields': ['content', 'title'],
                'highlight_pre_tag': '<mark>',
                'highlight_post_tag': '</mark>'
            }
            
            if facets:
                search_params['facets'] = facets
            
            results = self.search_client.search(**search_params)
            
            documents = []
            for result in results:
                doc = dict(result)
                # Add highlights if available
                if hasattr(result, '@search.highlights'):
                    doc['highlights'] = result['@search.highlights']
                documents.append(doc)
            
            facet_results = {}
            if facets and hasattr(results, 'get_facets'):
                facet_results = results.get_facets()
            
            return {
                'success': True,
                'query': query,
                'filters': filters,
                'total_count': results.get_count(),
                'documents': documents,
                'facets': facet_results,
                'page_info': {
                    'top': top,
                    'skip': skip,
                    'has_more': results.get_count() > (skip + len(documents))
                }
            }
            
        except Exception as e:
            logger.error(f"Error in advanced search: {e}")
            return {
                'success': False,
                'query': query,
                'error': str(e),
                'documents': [],
                'total_count': 0
            }
    
    def semantic_search(self, query: str, vector: List[float],
                       top: int = 50) -> Dict[str, Any]:
        """Perform semantic search using vectors"""
        try:
            vector_query = VectorizedQuery(
                vector=vector,
                k_nearest_neighbors=top,
                fields="content_vector"
            )
            
            results = self.search_client.search(
                search_text=query,
                vector_queries=[vector_query],
                top=top,
                include_total_count=True
            )
            
            documents = []
            for result in results:
                doc = dict(result)
                # Add semantic score if available
                if hasattr(result, '@search.score'):
                    doc['semantic_score'] = result['@search.score']
                documents.append(doc)
            
            return {
                'success': True,
                'query': query,
                'search_type': 'semantic',
                'total_count': results.get_count(),
                'documents': documents
            }
            
        except Exception as e:
            logger.error(f"Error in semantic search: {e}")
            return {
                'success': False,
                'query': query,
                'error': str(e),
                'documents': [],
                'total_count': 0
            }
    
    def suggest(self, query: str, suggester_name: str = "sg",
               top: int = 5) -> List[str]:
        """Get search suggestions"""
        try:
            results = self.search_client.suggest(
                search_text=query,
                suggester_name=suggester_name,
                top=top
            )
            
            suggestions = [result['@@search.text'] for result in results]
            return suggestions
            
        except Exception as e:
            logger.error(f"Error getting suggestions: {e}")
            return []
    
    def autocomplete(self, query: str, suggester_name: str = "sg",
                    mode: str = "oneTermWithContext") -> List[str]:
        """Get autocomplete suggestions"""
        try:
            results = self.search_client.autocomplete(
                search_text=query,
                suggester_name=suggester_name,
                autocomplete_mode=mode
            )
            
            completions = [result['text'] for result in results]
            return completions
            
        except Exception as e:
            logger.error(f"Error getting autocomplete: {e}")
            return []
    
    def get_document(self, key: str) -> Optional[Dict[str, Any]]:
        """Get a specific document by key"""
        try:
            result = self.search_client.get_document(key=key)
            return dict(result)
        except Exception as e:
            logger.error(f"Error getting document {key}: {e}")
            return None
    
    def count_documents(self, filters: Optional[str] = None) -> int:
        """Count documents matching filters"""
        try:
            results = self.search_client.search(
                search_text="*",
                filter=filters,
                top=0,
                include_total_count=True
            )
            return results.get_count()
        except Exception as e:
            logger.error(f"Error counting documents: {e}")
            return 0