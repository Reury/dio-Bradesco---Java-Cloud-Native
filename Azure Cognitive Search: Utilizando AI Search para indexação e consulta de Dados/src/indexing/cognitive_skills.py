from typing import Dict, Any, List, Optional
from azure.search.documents.indexes import SearchIndexerClient
from azure.search.documents.indexes.models import (
    SearchIndexerSkillset, OcrSkill, MergeSkill, EntityRecognitionSkill,
    KeyPhraseExtractionSkill, LanguageDetectionSkill, SentimentSkill,
    SplitSkill, InputFieldMappingEntry, OutputFieldMappingEntry
)
from azure.core.credentials import AzureKeyCredential
import logging

logger = logging.getLogger(__name__)

class CognitiveSkillsManager:
    """Manage cognitive skills for document enrichment"""
    
    def __init__(self, service_name: str, admin_key: str, 
                 cognitive_services_key: str):
        self.service_endpoint = f"https://{service_name}.search.windows.net"
        self.indexer_client = SearchIndexerClient(
            endpoint=self.service_endpoint,
            credential=AzureKeyCredential(admin_key)
        )
        self.cognitive_services_key = cognitive_services_key
    
    def create_skillset(self, skillset_name: str, 
                       skills_config: Dict[str, bool]) -> Dict[str, Any]:
        """Create a skillset with specified skills"""
        try:
            skills = []
            
            # OCR Skill
            if skills_config.get('ocr_enabled', False):
                skills.append(self._create_ocr_skill())
            
            # Language Detection
            if skills_config.get('language_detection', True):
                skills.append(self._create_language_detection_skill())
            
            # Text Split
            skills.append(self._create_text_split_skill())
            
            # Entity Recognition
            if skills_config.get('entity_extraction', True):
                skills.append(self._create_entity_recognition_skill())
            
            # Key Phrase Extraction
            if skills_config.get('key_phrase_extraction', True):
                skills.append(self._create_key_phrase_skill())
            
            # Sentiment Analysis
            if skills_config.get('sentiment_analysis', True):
                skills.append(self._create_sentiment_skill())
            
            # Merge enriched content
            skills.append(self._create_merge_skill())
            
            skillset = SearchIndexerSkillset(
                name=skillset_name,
                description="Document processing skillset with AI enrichment",
                skills=skills,
                cognitive_services_account=self.cognitive_services_key
            )
            
            result = self.indexer_client.create_skillset(skillset)
            logger.info(f"Created skillset: {skillset_name}")
            
            return {
                'success': True,
                'skillset_name': skillset_name,
                'skills_count': len(skills)
            }
            
        except Exception as e:
            logger.error(f"Error creating skillset {skillset_name}: {e}")
            return {
                'success': False,
                'skillset_name': skillset_name,
                'error': str(e)
            }
    
    def _create_ocr_skill(self) -> OcrSkill:
        """Create OCR skill for image text extraction"""
        return OcrSkill(
            name="ocr",
            description="Extract text from images",
            context="/document/normalized_images/*",
            inputs=[
                InputFieldMappingEntry(name="image", source="/document/normalized_images/*")
            ],
            outputs=[
                OutputFieldMappingEntry(name="text", target_name="text"),
                OutputFieldMappingEntry(name="layoutText", target_name="layoutText")
            ]
        )
    
    def _create_language_detection_skill(self) -> LanguageDetectionSkill:
        """Create language detection skill"""
        return LanguageDetectionSkill(
            name="languagedetection",
            description="Detect document language",
            context="/document",
            inputs=[
                InputFieldMappingEntry(name="text", source="/document/content")
            ],
            outputs=[
                OutputFieldMappingEntry(name="languageCode", target_name="languageCode"),
                OutputFieldMappingEntry(name="languageName", target_name="languageName")
            ]
        )
    
    def _create_text_split_skill(self) -> SplitSkill:
        """Create text splitting skill for large documents"""
        return SplitSkill(
            name="textsplit",
            description="Split text into chunks",
            context="/document",
            text_split_mode="pages",
            maximum_page_length=4000,
            inputs=[
                InputFieldMappingEntry(name="text", source="/document/content"),
                InputFieldMappingEntry(name="languageCode", source="/document/languageCode")
            ],
            outputs=[
                OutputFieldMappingEntry(name="textItems", target_name="pages")
            ]
        )
    
    def _create_entity_recognition_skill(self) -> EntityRecognitionSkill:
        """Create entity recognition skill"""
        return EntityRecognitionSkill(
            name="entityrecognition",
            description="Extract entities from text",
            context="/document/pages/*",
            categories=["Person", "Location", "Organization", "Datetime", "Email", "URL"],
            inputs=[
                InputFieldMappingEntry(name="text", source="/document/pages/*"),
                InputFieldMappingEntry(name="languageCode", source="/document/languageCode")
            ],
            outputs=[
                OutputFieldMappingEntry(name="persons", target_name="persons"),
                OutputFieldMappingEntry(name="locations", target_name="locations"),
                OutputFieldMappingEntry(name="organizations", target_name="organizations"),
                OutputFieldMappingEntry(name="entities", target_name="entities")
            ]
        )
    
    def _create_key_phrase_skill(self) -> KeyPhraseExtractionSkill:
        """Create key phrase extraction skill"""
        return KeyPhraseExtractionSkill(
            name="keyphraseextraction",
            description="Extract key phrases",
            context="/document/pages/*",
            inputs=[
                InputFieldMappingEntry(name="text", source="/document/pages/*"),
                InputFieldMappingEntry(name="languageCode", source="/document/languageCode")
            ],
            outputs=[
                OutputFieldMappingEntry(name="keyPhrases", target_name="keyPhrases")
            ]
        )
    
    def _create_sentiment_skill(self) -> SentimentSkill:
        """Create sentiment analysis skill"""
        return SentimentSkill(
            name="sentimentanalysis",
            description="Analyze sentiment",
            context="/document/pages/*",
            inputs=[
                InputFieldMappingEntry(name="text", source="/document/pages/*"),
                InputFieldMappingEntry(name="languageCode", source="/document/languageCode")
            ],
            outputs=[
                OutputFieldMappingEntry(name="score", target_name="sentimentScore"),
                OutputFieldMappingEntry(name="sentiment", target_name="sentiment")
            ]
        )
    
    def _create_merge_skill(self) -> MergeSkill:
        """Create merge skill to combine enriched content"""
        return MergeSkill(
            name="mergetext",
            description="Merge enriched content",
            context="/document",
            insert_pre_tag=" ",
            insert_post_tag=" ",
            inputs=[
                InputFieldMappingEntry(name="text", source="/document/content"),
                InputFieldMappingEntry(name="itemsToInsert", source="/document/pages/*/keyPhrases/*"),
                InputFieldMappingEntry(name="offsets", source="/document/pages/*/offset")
            ],
            outputs=[
                OutputFieldMappingEntry(name="mergedText", target_name="merged_content")
            ]
        )
    
    def list_skillsets(self) -> List[str]:
        """List all skillsets"""
        try:
            skillsets = self.indexer_client.get_skillsets()
            return [skillset.name for skillset in skillsets]
        except Exception as e:
            logger.error(f"Error listing skillsets: {e}")
            return []
    
    def delete_skillset(self, skillset_name: str) -> Dict[str, Any]:
        """Delete a skillset"""
        try:
            self.indexer_client.delete_skillset(skillset_name)
            logger.info(f"Deleted skillset: {skillset_name}")
            return {'success': True, 'skillset_name': skillset_name}
        except Exception as e:
            logger.error(f"Error deleting skillset {skillset_name}: {e}")
            return {'success': False, 'skillset_name': skillset_name, 'error': str(e)}