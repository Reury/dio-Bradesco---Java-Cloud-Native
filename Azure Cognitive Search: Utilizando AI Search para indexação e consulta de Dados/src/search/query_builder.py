from typing import Dict, Any, List, Optional, Union
from datetime import datetime, date
import logging

logger = logging.getLogger(__name__)

class QueryBuilder:
    """Build complex search queries programmatically"""
    
    def __init__(self):
        self.query_parts = []
        self.filters = []
        self.facets = []
        self.order_by = []
        self.highlight_fields = []
    
    def add_term(self, term: str, field: Optional[str] = None,
                boost: Optional[float] = None) -> 'QueryBuilder':
        """Add a search term"""
        if field:
            query_part = f"{field}:{term}"
        else:
            query_part = term
        
        if boost:
            query_part += f"^{boost}"
        
        self.query_parts.append(query_part)
        return self
    
    def add_phrase(self, phrase: str, field: Optional[str] = None,
                  slop: Optional[int] = None) -> 'QueryBuilder':
        """Add a phrase search"""
        quoted_phrase = f'"{phrase}"'
        
        if slop:
            quoted_phrase += f"~{slop}"
        
        if field:
            query_part = f"{field}:{quoted_phrase}"
        else:
            query_part = quoted_phrase
        
        self.query_parts.append(query_part)
        return self
    
    def add_wildcard(self, pattern: str, field: Optional[str] = None) -> 'QueryBuilder':
        """Add wildcard search"""
        if field:
            query_part = f"{field}:{pattern}"
        else:
            query_part = pattern
        
        self.query_parts.append(query_part)
        return self
    
    def add_fuzzy(self, term: str, field: Optional[str] = None,
                 fuzziness: int = 1) -> 'QueryBuilder':
        """Add fuzzy search"""
        fuzzy_term = f"{term}~{fuzziness}"
        
        if field:
            query_part = f"{field}:{fuzzy_term}"
        else:
            query_part = fuzzy_term
        
        self.query_parts.append(query_part)
        return self
    
    def add_range(self, field: str, min_val: Union[str, int, float, datetime],
                 max_val: Union[str, int, float, datetime],
                 include_min: bool = True, include_max: bool = True) -> 'QueryBuilder':
        """Add range search"""
        min_bracket = "[" if include_min else "{"
        max_bracket = "]" if include_max else "}"
        
        # Format datetime values
        if isinstance(min_val, (datetime, date)):
            min_val = min_val.isoformat()
        if isinstance(max_val, (datetime, date)):
            max_val = max_val.isoformat()
        
        query_part = f"{field}:{min_bracket}{min_val} TO {max_val}{max_bracket}"
        self.query_parts.append(query_part)
        return self
    
    def add_filter(self, field: str, operator: str, value: Any) -> 'QueryBuilder':
        """Add OData filter"""
        if operator.lower() == 'eq':
            if isinstance(value, str):
                filter_expr = f"{field} eq '{value}'"
            else:
                filter_expr = f"{field} eq {value}"
        elif operator.lower() == 'ne':
            if isinstance(value, str):
                filter_expr = f"{field} ne '{value}'"
            else:
                filter_expr = f"{field} ne {value}"
        elif operator.lower() in ['gt', 'ge', 'lt', 'le']:
            if isinstance(value, (datetime, date)):
                value = value.isoformat()
            filter_expr = f"{field} {operator} {value}"
        elif operator.lower() == 'in':
            if isinstance(value, list):
                value_list = ','.join([f"'{v}'" if isinstance(v, str) else str(v) for v in value])
                filter_expr = f"{field}/any(x: search.in(x, '{value_list}', ','))"
            else:
                raise ValueError("Value must be a list for 'in' operator")
        else:
            raise ValueError(f"Unsupported operator: {operator}")
        
        self.filters.append(filter_expr)
        return self
    
    def add_text_filter(self, field: str, text: str, operator: str = 'contains') -> 'QueryBuilder':
        """Add text-based filter"""
        if operator.lower() == 'contains':
            filter_expr = f"search.ismatch('{text}', '{field}')"
        elif operator.lower() == 'startswith':
            filter_expr = f"startswith({field}, '{text}')"
        elif operator.lower() == 'endswith':
            filter_expr = f"endswith({field}, '{text}')"
        else:
            raise ValueError(f"Unsupported text operator: {operator}")
        
        self.filters.append(filter_expr)
        return self
    
    def add_facet(self, field: str, count: Optional[int] = None,
                 sort: Optional[str] = None) -> 'QueryBuilder':
        """Add facet configuration"""
        facet_config = field
        
        params = []
        if count:
            params.append(f"count:{count}")
        if sort:
            params.append(f"sort:{sort}")
        
        if params:
            facet_config += f",{','.join(params)}"
        
        self.facets.append(facet_config)
        return self
    
    def add_sort(self, field: str, direction: str = 'asc') -> 'QueryBuilder':
        """Add sorting"""
        sort_expr = f"{field} {direction}"
        self.order_by.append(sort_expr)
        return self
    
    def add_highlight(self, field: str) -> 'QueryBuilder':
        """Add field to highlight"""
        self.highlight_fields.append(field)
        return self
    
    def build_query(self) -> str:
        """Build the final query string"""
        if not self.query_parts:
            return "*"
        
        return " ".join(self.query_parts)
    
    def build_filter(self) -> Optional[str]:
        """Build the filter string"""
        if not self.filters:
            return None
        
        return " and ".join(self.filters)
    
    def build_facets(self) -> List[str]:
        """Build facets list"""
        return self.facets
    
    def build_order_by(self) -> List[str]:
        """Build order by list"""
        return self.order_by
    
    def build_highlight_fields(self) -> List[str]:
        """Build highlight fields list"""
        return self.highlight_fields
    
    def build_search_params(self) -> Dict[str, Any]:
        """Build complete search parameters"""
        params = {
            'search_text': self.build_query()
        }
        
        filter_expr = self.build_filter()
        if filter_expr:
            params['filter'] = filter_expr
        
        if self.facets:
            params['facets'] = self.build_facets()
        
        if self.order_by:
            params['order_by'] = self.build_order_by()
        
        if self.highlight_fields:
            params['highlight_fields'] = self.build_highlight_fields()
        
        return params
    
    def reset(self) -> 'QueryBuilder':
        """Reset the query builder"""
        self.query_parts = []
        self.filters = []
        self.facets = []
        self.order_by = []
        self.highlight_fields = []
        return self

# Convenience functions
def create_simple_query(terms: List[str]) -> str:
    """Create a simple query from terms"""
    return QueryBuilder().add_term(" ".join(terms)).build_query()

def create_filtered_query(query: str, filters: Dict[str, Any]) -> Dict[str, Any]:
    """Create a query with filters"""
    builder = QueryBuilder().add_term(query)
    
    for field, value in filters.items():
        if isinstance(value, list):
            builder.add_filter(field, 'in', value)
        else:
            builder.add_filter(field, 'eq', value)
    
    return builder.build_search_params()