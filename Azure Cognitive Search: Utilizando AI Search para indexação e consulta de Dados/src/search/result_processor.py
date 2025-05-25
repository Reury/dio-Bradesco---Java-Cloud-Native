from typing import Dict, Any, List, Optional, Union
import pandas as pd
import json
from collections import Counter, defaultdict
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class SearchResultProcessor:
    """Process and analyze search results"""
    
    def __init__(self):
        self.results_cache = {}
    
    def process_results(self, search_results: Dict[str, Any]) -> Dict[str, Any]:
        """Process raw search results and add analytics"""
        if not search_results.get('success', False):
            return search_results
        
        documents = search_results.get('documents', [])
        
        processed_results = {
            **search_results,
            'analytics': self._generate_analytics(documents),
            'processed_at': datetime.now().isoformat(),
            'processing_info': {
                'total_processed': len(documents),
                'has_highlights': any('highlights' in doc for doc in documents),
                'has_scores': any('@search.score' in doc for doc in documents)
            }
        }
        
        return processed_results
    
    def _generate_analytics(self, documents: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate analytics from search results"""
        if not documents:
            return {}
        
        analytics = {
            'document_count': len(documents),
            'category_distribution': self._analyze_categories(documents),
            'language_distribution': self._analyze_languages(documents),
            'date_distribution': self._analyze_dates(documents),
            'score_statistics': self._analyze_scores(documents),
            'content_statistics': self._analyze_content(documents),
            'entity_analysis': self._analyze_entities(documents)
        }
        
        return analytics
    
    def _analyze_categories(self, documents: List[Dict[str, Any]]) -> Dict[str, int]:
        """Analyze category distribution"""
        categories = []
        for doc in documents:
            category = doc.get('category', 'Unknown')
            if isinstance(category, list):
                categories.extend(category)
            else:
                categories.append(category)
        
        return dict(Counter(categories))
    
    def _analyze_languages(self, documents: List[Dict[str, Any]]) -> Dict[str, int]:
        """Analyze language distribution"""
        languages = []
        for doc in documents:
            language = doc.get('language') or doc.get('languageCode', 'Unknown')
            languages.append(language)
        
        return dict(Counter(languages))
    
    def _analyze_dates(self, documents: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze date distribution"""
        dates = []
        date_fields = ['created_date', 'modified_date', 'published_date']
        
        for doc in documents:
            for field in date_fields:
                if field in doc and doc[field]:
                    try:
                        if isinstance(doc[field], str):
                            date_obj = datetime.fromisoformat(doc[field].replace('Z', '+00:00'))
                        else:
                            date_obj = doc[field]
                        dates.append(date_obj)
                        break
                    except (ValueError, TypeError):
                        continue
        
        if not dates:
            return {}
        
        # Group by year-month
        date_groups = defaultdict(int)
        for date_obj in dates:
            year_month = f"{date_obj.year}-{date_obj.month:02d}"
            date_groups[year_month] += 1
        
        return {
            'total_documents_with_dates': len(dates),
            'date_range': {
                'earliest': min(dates).isoformat() if dates else None,
                'latest': max(dates).isoformat() if dates else None
            },
            'monthly_distribution': dict(date_groups)
        }
    
    def _analyze_scores(self, documents: List[Dict[str, Any]]) -> Dict[str, float]:
        """Analyze search scores"""
        scores = []
        for doc in documents:
            score = doc.get('@search.score')
            if score is not None:
                scores.append(float(score))
        
        if not scores:
            return {}
        
        return {
            'min_score': min(scores),
            'max_score': max(scores),
            'avg_score': sum(scores) / len(scores),
            'score_distribution': {
                'high_relevance': len([s for s in scores if s > 0.8]),
                'medium_relevance': len([s for s in scores if 0.4 <= s <= 0.8]),
                'low_relevance': len([s for s in scores if s < 0.4])
            }
        }
    
    def _analyze_content(self, documents: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze content statistics"""
        content_lengths = []
        file_types = []
        
        for doc in documents:
            content = doc.get('content', '')
            if content:
                content_lengths.append(len(content))
            
            file_type = doc.get('file_type') or doc.get('content_type', 'Unknown')
            file_types.append(file_type)
        
        stats = {
            'file_type_distribution': dict(Counter(file_types))
        }
        
        if content_lengths:
            stats.update({
                'content_length_stats': {
                    'min_length': min(content_lengths),
                    'max_length': max(content_lengths),
                    'avg_length': sum(content_lengths) / len(content_lengths),
                    'total_characters': sum(content_lengths)
                }
            })
        
        return stats
    
    def _analyze_entities(self, documents: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze extracted entities"""
        all_entities = {
            'persons': [],
            'locations': [],
            'organizations': [],
            'emails': [],
            'urls': []
        }
        
        for doc in documents:
            for entity_type in all_entities.keys():
                entities = doc.get(entity_type, [])
                if isinstance(entities, list):
                    all_entities[entity_type].extend(entities)
                elif entities:  # Single entity
                    all_entities[entity_type].append(entities)
        
        entity_stats = {}
        for entity_type, entities in all_entities.items():
            if entities:
                entity_counter = Counter(entities)
                entity_stats[entity_type] = {
                    'total_count': len(entities),
                    'unique_count': len(entity_counter),
                    'top_entities': dict(entity_counter.most_common(10))
                }
        
        return entity_stats
    
    def export_to_dataframe(self, search_results: Dict[str, Any]) -> pd.DataFrame:
        """Export search results to pandas DataFrame"""
        documents = search_results.get('documents', [])
        if not documents:
            return pd.DataFrame()
        
        # Flatten nested structures for DataFrame
        flattened_docs = []
        for doc in documents:
            flat_doc = {}
            for key, value in doc.items():
                if isinstance(value, (list, dict)):
                    flat_doc[key] = json.dumps(value) if value else None
                else:
                    flat_doc[key] = value
            flattened_docs.append(flat_doc)
        
        df = pd.DataFrame(flattened_docs)
        return df
    
    def export_to_csv(self, search_results: Dict[str, Any], 
                     filename: str, include_metadata: bool = True) -> bool:
        """Export search results to CSV file"""
        try:
            df = self.export_to_dataframe(search_results)
            
            if not include_metadata:
                # Remove metadata columns
                metadata_cols = [col for col in df.columns if col.startswith('@')]
                df = df.drop(columns=metadata_cols, errors='ignore')
            
            df.to_csv(filename, index=False, encoding='utf-8')
            logger.info(f"Exported {len(df)} results to {filename}")
            return True
            
        except Exception as e:
            logger.error(f"Error exporting to CSV: {e}")
            return False
    
    def export_to_json(self, search_results: Dict[str, Any], 
                      filename: str, pretty: bool = True) -> bool:
        """Export search results to JSON file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                if pretty:
                    json.dump(search_results, f, indent=2, ensure_ascii=False, default=str)
                else:
                    json.dump(search_results, f, ensure_ascii=False, default=str)
            
            logger.info(f"Exported results to {filename}")
            return True
            
        except Exception as e:
            logger.error(f"Error exporting to JSON: {e}")
            return False
    
    def filter_results(self, search_results: Dict[str, Any], 
                      filters: Dict[str, Any]) -> Dict[str, Any]:
        """Filter search results based on criteria"""
        documents = search_results.get('documents', [])
        filtered_docs = []
        
        for doc in documents:
            include_doc = True
            
            for field, criteria in filters.items():
                doc_value = doc.get(field)
                
                if isinstance(criteria, dict):
                    # Handle range filters
                    if 'min' in criteria and doc_value is not None:
                        if doc_value < criteria['min']:
                            include_doc = False
                            break
                    if 'max' in criteria and doc_value is not None:
                        if doc_value > criteria['max']:
                            include_doc = False
                            break
                    # Handle list filters
                    if 'in' in criteria:
                        if doc_value not in criteria['in']:
                            include_doc = False
                            break
                else:
                    # Exact match
                    if doc_value != criteria:
                        include_doc = False
                        break
            
            if include_doc:
                filtered_docs.append(doc)
        
        filtered_results = {
            **search_results,
            'documents': filtered_docs,
            'total_count': len(filtered_docs),
            'original_count': len(documents),
            'filter_applied': filters
        }
        
        return filtered_results
    
    def sort_results(self, search_results: Dict[str, Any], 
                    sort_field: str, reverse: bool = False) -> Dict[str, Any]:
        """Sort search results by field"""
        documents = search_results.get('documents', [])
        
        try:
            sorted_docs = sorted(
                documents,
                key=lambda x: x.get(sort_field, ''),
                reverse=reverse
            )
            
            sorted_results = {
                **search_results,
                'documents': sorted_docs,
                'sort_applied': {
                    'field': sort_field,
                    'reverse': reverse
                }
            }
            
            return sorted_results
            
        except Exception as e:
            logger.error(f"Error sorting results: {e}")
            return search_results
    
    def paginate_results(self, search_results: Dict[str, Any], 
                        page: int, page_size: int = 20) -> Dict[str, Any]:
        """Paginate search results"""
        documents = search_results.get('documents', [])
        total_docs = len(documents)
        
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        
        paginated_docs = documents[start_idx:end_idx]
        
        paginated_results = {
            **search_results,
            'documents': paginated_docs,
            'pagination': {
                'page': page,
                'page_size': page_size,
                'total_pages': (total_docs + page_size - 1) // page_size,
                'total_documents': total_docs,
                'has_next': end_idx < total_docs,
                'has_previous': page > 1
            }
        }
        
        return paginated_results
    
    def highlight_content(self, content: str, terms: List[str], 
                         pre_tag: str = '<mark>', 
                         post_tag: str = '</mark>') -> str:
        """Highlight search terms in content"""
        highlighted_content = content
        
        for term in terms:
            # Case-insensitive replacement
            import re
            pattern = re.compile(re.escape(term), re.IGNORECASE)
            highlighted_content = pattern.sub(
                f"{pre_tag}{term}{post_tag}", 
                highlighted_content
            )
        
        return highlighted_content
    
    def get_search_insights(self, search_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate insights from search results"""
        documents = search_results.get('documents', [])
        query = search_results.get('query', '')
        
        insights = {
            'query_analysis': {
                'query': query,
                'query_length': len(query.split()),
                'has_operators': any(op in query.lower() for op in ['and', 'or', 'not', '"', '*', '~']),
            },
            'result_quality': {
                'total_results': len(documents),
                'has_high_relevance': any(
                    doc.get('@search.score', 0) > 0.8 for doc in documents
                ),
                'diversity_score': len(set(doc.get('category', '') for doc in documents))
            },
            'content_insights': self._get_content_insights(documents),
            'recommendations': self._get_search_recommendations(search_results)
        }
        
        return insights
    
    def _get_content_insights(self, documents: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Extract insights from document content"""
        if not documents:
            return {}
        
        # Extract key phrases from all documents
        all_key_phrases = []
        for doc in documents:
            key_phrases = doc.get('keyPhrases', [])
            if isinstance(key_phrases, list):
                all_key_phrases.extend(key_phrases)
        
        # Get most common themes
        phrase_counter = Counter(all_key_phrases)
        
        return {
            'common_themes': dict(phrase_counter.most_common(10)),
            'total_key_phrases': len(all_key_phrases),
            'unique_key_phrases': len(phrase_counter)
        }
    
    def _get_search_recommendations(self, search_results: Dict[str, Any]) -> List[str]:
        """Generate search recommendations"""
        recommendations = []
        documents = search_results.get('documents', [])
        total_count = search_results.get('total_count', 0)
        
        if total_count == 0:
            recommendations.extend([
                "Try using different or more general search terms",
                "Check for spelling errors in your query",
                "Remove filters to broaden your search"
            ])
        elif total_count > 1000:
            recommendations.extend([
                "Consider adding filters to narrow down results",
                "Use more specific search terms",
                "Try using phrase searches with quotes"
            ])
        elif len(documents) < 10:
            recommendations.extend([
                "Try using broader search terms",
                "Use wildcard searches with * for partial matches",
                "Consider using fuzzy search for similar terms"
            ])
        
        # Category-based recommendations
        categories = set(doc.get('category', '') for doc in documents)
        if len(categories) > 1:
            recommendations.append(f"Filter by category: {', '.join(categories)}")
        
        return recommendations