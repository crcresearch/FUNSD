from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field


class QuestionType(str, Enum):
    """Types of questions in the FUNSD_QA dataset."""
    EXTRACTION = "extraction"
    ENTITY_DETECTION = "entity_detection"
    RELATIONSHIP = "relationship"
    NUMERICAL_REASONING = "numerical_reasoning"
    TEMPORAL_REASONING = "temporal_reasoning"
    LAYOUT_UNDERSTANDING = "layout_understanding"
    MULTI_HOP_REASONING = "multi_hop_reasoning"
    CLASSIFICATION = "classification"
    VERIFICATION = "verification"
    SUMMARIZATION = "summarization"
    # New question types
    COMPARATIVE_REASONING = "comparative_reasoning"
    COUNTERFACTUAL_REASONING = "counterfactual_reasoning"
    VISUAL_REASONING = "visual_reasoning"


class DifficultyLevel(str, Enum):
    """Difficulty levels for questions."""
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class GenerationMethod(str, Enum):
    """Methods used to generate the QA pairs."""
    MANUAL = "manual"
    SEMI_AUTOMATED = "semi_automated"
    AUTOMATED = "automated"


class DocumentRelationType(str, Enum):
    """Types of relationships between documents in multi-document questions."""
    CHRONOLOGICAL = "chronological"  # Time-based relationship (e.g., versions, updates)
    COMPLEMENTARY = "complementary"  # Different aspects of same entity or process
    CONTRADICTORY = "contradictory"  # Documents with conflicting information
    PREREQUISITE = "prerequisite"    # One document needed to understand another


class InformationSynthesisComplexity(str, Enum):
    """Complexity levels for synthesizing information across documents."""
    LOW = "low"        # Simple extraction and combination
    MEDIUM = "medium"  # Requires some inference or calculation
    HIGH = "high"      # Complex reasoning across multiple sources


class SupportingSection(BaseModel):
    """A section within a document that supports answering the question."""
    document_id: str = Field(..., description="ID of the document containing this section")
    section: str = Field(..., description="Name of the section within the document")


class FUNSDQAPair(BaseModel):
    """
    Schema for a question-answer pair in the FUNSD_QA dataset.
    Supports both single-document and multi-document QA pairs.
    """
    # Core identification fields
    id: str = Field(..., description="Unique identifier for the QA pair")
    
    # Question fields - hybrid approach for RAG evaluation
    reference_question: str = Field(..., description="Clean, focused question for evaluation scoring")
    user_question: str = Field(..., description="Question with document context for RAG retrieval")
    answer: str = Field(..., description="Answer to the question")
    
    # Classification fields
    type: QuestionType = Field(..., description="Type of question/reasoning required")
    difficulty: DifficultyLevel = Field(..., description="Difficulty level of the question")
    
    # Document reference fields
    supporting_documents: List[str] = Field(..., description="List of document IDs needed to answer the question")
    section: str = Field(..., description="Primary section where the answer is found")
    
    # Optional detail fields
    supporting_sections: Optional[List[SupportingSection]] = Field(None, description="Specific sections within documents needed for the answer")
    reasoning_path: Optional[List[str]] = Field(None, description="Step-by-step reasoning process to arrive at the answer")
    context: Optional[str] = Field(None, description="Relevant context from the document(s) for answering the question")
    requires_reasoning: bool = Field(..., description="Whether the question requires reasoning beyond simple extraction")
    
    # Multi-document specific fields
    document_relationship_type: Optional[DocumentRelationType] = Field(None, 
        description="For multi-document questions, the relationship type between documents")
    information_synthesis_complexity: Optional[InformationSynthesisComplexity] = Field(None,
        description="For multi-document questions, the complexity of synthesizing information")
    
    # Visual reasoning fields
    requires_image: Optional[bool] = Field(None, description="Whether answering requires the document image (not just text)")
    visual_elements: Optional[List[str]] = Field(None, description="Visual elements relevant to answering the question")
    
    # Metadata fields
    generation_method: GenerationMethod = Field(..., description="Method used to generate this QA pair")
    verified: bool = Field(..., description="Whether this QA pair has been manually verified")
    
    class Config:
        """Pydantic model configuration."""
        schema_extra = {
            "example": {
                "id": "qa_multihop_001",
                "reference_question": "What is the Tipping Paper substance measurement for the product manufactured in NICOSIA?",
                "user_question": "What is the Tipping Paper substance measurement for the PHOENIX cigarettes manufactured in NICOSIA according to the B.A.T. CYPRUS specification?",
                "answer": "36 gm/m²",
                "type": "multi_hop_reasoning",
                "difficulty": "hard",
                "supporting_documents": ["0000989556"],
                "supporting_sections": [
                    {"document_id": "0000989556", "section": "PRODUCT SPECIFICATION"},
                    {"document_id": "0000989556", "section": "Tipping and Tipping Application"}
                ],
                "reasoning_path": [
                    "Identify the manufacturing location in the PRODUCT SPECIFICATION section (NICOSIA)",
                    "Find the tipping paper specifications in the Tipping and Tipping Application section",
                    "Extract the substance measurement value (36 gm/m²)"
                ],
                "section": "Tipping and Tipping Application",
                "context": "Place of Manufacture: NICOSIA\n\n...\n\nSubstance: 36 | gm/m²",
                "requires_reasoning": True,
                "generation_method": "manual",
                "verified": True
            }
        }


class FUNSDQADataset(BaseModel):
    """Collection of QA pairs forming a dataset."""
    qa_pairs: List[FUNSDQAPair] = Field(..., description="List of question-answer pairs")
    
    class Config:
        """Pydantic model configuration."""
        schema_extra = {
            "example": {
                "qa_pairs": [
                    {
                        "id": "qa_extraction_001",
                        "reference_question": "What is the brand name listed in the product specification?",
                        "user_question": "What is the brand name listed in the B.A.T. CYPRUS cigarette product specification from 1985?",
                        "answer": "PHOENIX",
                        "type": "extraction",
                        "difficulty": "easy",
                        "supporting_documents": ["0000989556"],
                        "section": "PRODUCT SPECIFICATION",
                        "context": "Brand: PHOENIX\nStyle: KS8 - KS",
                        "requires_reasoning": False,
                        "generation_method": "manual",
                        "verified": True
                    }
                ]
            }
        }


# Example usage:
"""
# Load QA pairs from JSON
import json
from pathlib import Path

def load_qa_dataset(filepath: str) -> FUNSDQADataset:
    '''Load QA dataset from a JSON file and validate against the schema.'''
    data = json.loads(Path(filepath).read_text())
    return FUNSDQADataset(qa_pairs=data)

# You can load a dataset file like this:
# dataset = load_qa_dataset("datasets/FUNSD_QA/training/qa_pairs_0000989556.json")

# To validate a single QA pair:
# qa_pair = FUNSDQAPair(**json_data)

# To convert back to JSON:
# json_string = dataset.json(indent=2)
""" 