from typing import List, Dict, Any, Optional
from azure.search.documents.indexes.models import (
    SimpleField, SearchableField, ComplexField, 
    SearchFieldDataType, VectorSearchField, VectorSearchDimensions
)
import logging

logger = logging.getLogger(__name__)

class IndexSchemaBuilder:
    """Build search index schemas dynamically"""
    
    def __init__(self):
        self.fields = []
        self.field_names = set()
    
    def add_field(self, name: str, data_type: str, **kwargs) -> 'IndexSchemaBuilder':
        """Add a field to the schema"""
        if name in self.field_names:
            logger.warning(f"Field {name} already exists, skipping")
            return self
        
        # Map data type string to SearchFieldDataType
        type_mapping = {
            "Edm.String": SearchFieldDataType.String,
            "Edm.Int32": SearchFieldDataType.Int32,
            "Edm.Int64": SearchFieldDataType.Int64,
            "Edm.Double": SearchFieldDataType.Double,
            "Edm.Boolean": SearchFieldDataType.Boolean,
            "Edm.DateTimeOffset": SearchFieldDataType.DateTimeOffset,
            "Edm.GeographyPoint": SearchFieldDataType.GeographyPoint,
            "Collection(Edm.String)": SearchFieldDataType.Collection(SearchFieldDataType.String)
        }
        
        field_type = type_mapping.get(data_type, SearchFieldDataType.String)
        
        # Determine if field should be searchable
        searchable = kwargs.get('searchable', False)
        
        if searchable and field_type == SearchFieldDataType.String:
            field = SearchableField(
                name=name,
                type=field_type,
                key=kwargs.get('key', False),
                filterable=kwargs.get('filterable', False),
                sortable=kwargs.get('sortable', False),
                facetable=kwargs.get('facetable', False),
                analyzer_name=kwargs.get('analyzer', None)
            )
        else:
            field = SimpleField(
                name=name,
                type=field_type,
                key=kwargs.get('key', False),
                filterable=kwargs.get('filterable', False),
                sortable=kwargs.get('sortable', False),
                facetable=kwargs.get('facetable', False)
            )
        
        self.fields.append(field)
        self.field_names.add(name)
        logger.info(f"Added field: {name} ({data_type})")
        
        return self
    
    def add_complex_field(self, name: str, fields: List[Any]) -> 'IndexSchemaBuilder':
        """Add a complex field with nested structure"""
        if name in self.field_names:
            logger.warning(f"Complex field {name} already exists, skipping")
            return self
        
        complex_field = ComplexField(name=name, fields=fields)
        self.fields.append(complex_field)
        self.field_names.add(name)
        logger.info(f"Added complex field: {name}")
        
        return self
    
    def add_vector_field(self, name: str, dimensions: int, 
                        vector_search_profile_name: str) -> 'IndexSchemaBuilder':
        """Add a vector field for semantic search"""
        if name in self.field_names:
            logger.warning(f"Vector field {name} already exists, skipping")
            return self
        
        vector_field = VectorSearchField(
            name=name,
            type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
            searchable=True,
            vector_search_dimensions=dimensions,
            vector_search_profile_name=vector_search_profile_name
        )
        
        self.fields.append(vector_field)
        self.field_names.add(name)
        logger.info(f"Added vector field: {name} ({dimensions} dimensions)")
        
        return self
    
    def build(self) -> List[Any]:
        """Build and return the complete field list"""
        if not self.fields:
            logger.warning("No fields defined in schema")
        
        return self.fields
    
    def get_document_schema(self) -> 'IndexSchemaBuilder':
        """Get a pre-defined document schema"""
        self.add_field("id", "Edm.String", key=True)
        self.add_field("title", "Edm.String", searchable=True, filterable=True)
        self.add_field("content", "Edm.String", searchable=True)
        self.add_field("category", "Edm.String", filterable=True, facetable=True)
        self.add_field("tags", "Collection(Edm.String)", searchable=True, filterable=True)
        self.add_field("created_date", "Edm.DateTimeOffset", sortable=True, filterable=True)
        self.add_field("modified_date", "Edm.DateTimeOffset", sortable=True, filterable=True)
        self.add_field("file_size", "Edm.Int64", sortable=True, filterable=True)
        self.add_field("file_type", "Edm.String", filterable=True, facetable=True)
        self.add_field("language", "Edm.String", filterable=True, facetable=True)
        
        return self
    
    def reset(self) -> 'IndexSchemaBuilder':
        """Reset the schema builder"""
        self.fields = []
        self.field_names = set()
        return self