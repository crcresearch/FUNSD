# Question-Answer Pair Types

This document describes the different types of question-answer pairs in the FUNSD_QA dataset.

## 1. Extraction
Simple extraction of values from clearly labeled fields.

**Example:**
```json
{
  "id": "qa_extraction_001",
  "document_id": "0000989556",
  "question": "What is the brand name listed in the product specification?",
  "answer": "PHOENIX",
  "type": "extraction"
}
```

## 2. Entity Detection
Identifying specific entities or fields on the form.

**Example:**
```json
{
  "id": "qa_entity_001",
  "document_id": "0000989556",
  "question": "Does this form contain a filter specifications section?",
  "answer": "Yes",
  "type": "entity_detection"
}
```

## 3. Relationship
Understanding connections between different fields or entities.

**Example:**
```json
{
  "id": "qa_relationship_001",
  "document_id": "0000989556",
  "question": "What company manufactures the PHOENIX brand?",
  "answer": "B.A.T. CYPRUS",
  "type": "relationship"
}
```

## 4. Numerical Reasoning
Performing calculations or comparisons with numeric values.

**Example:**
```json
{
  "id": "qa_numerical_001",
  "document_id": "0000989556",
  "question": "What is the difference between Total Pressure Drop (encap.) and Total Pressure Drop (unencap.)?",
  "answer": "40 mm",
  "type": "numerical_reasoning"
}
```

## 5. Temporal Reasoning
Understanding date-related information and chronology.

**Example:**
```json
{
  "id": "qa_temporal_001",
  "document_id": "0000989556",
  "question": "When was this product specification prepared?",
  "answer": "May 1, 1985",
  "type": "temporal_reasoning"
}
```

## 6. Layout Understanding
Questions about the structural arrangement of the document.

**Example:**
```json
{
  "id": "qa_layout_001",
  "document_id": "0000989556",
  "question": "What section appears directly below the 'CIGARETTE MAKING' heading?",
  "answer": "Physical Characteristics",
  "type": "layout_understanding"
}
```

## 7. Multi-hop Reasoning
Requiring multiple steps to arrive at the answer.

**Example:**
```json
{
  "id": "qa_multihop_001",
  "document_id": "0000989556",
  "question": "What is the Tipping Paper substance measurement for the product manufactured in NICOSIA?",
  "answer": "36 gm/m²",
  "type": "multi_hop_reasoning"
}
```

## 8. Classification
Categorizing the document or information within it.

**Example:**
```json
{
  "id": "qa_classification_001",
  "document_id": "0000989556",
  "question": "What type of document is this?",
  "answer": "Product Specification",
  "type": "classification"
}
```

## 9. Verification
Confirming or disproving statements about the document.

**Example:**
```json
{
  "id": "qa_verification_001",
  "document_id": "0000989556",
  "question": "Is it true that the cigarette has a filter ventilation rate of 10%?",
  "answer": "False, it has a Nil filter ventilation rate",
  "type": "verification"
}
```

## 10. Summarization
Creating concise summaries of document sections.

**Example:**
```json
{
  "id": "qa_summarization_001",
  "document_id": "0000989556",
  "question": "Summarize the Physical Characteristics section.",
  "answer": "The section details cigarette dimensions including length (84mm), rod length (64mm), filter length (20mm), and various pressure measurements. It also specifies circumference (24.75mm), moisture content (13.5%), and notes no filter ventilation.",
  "type": "summarization"
}
```

## 11. Comparative Reasoning
Comparing information across multiple documents or sections to identify similarities, differences, or patterns.

**Example:**
```json
{
  "id": "qa_comparative_001",
  "supporting_documents": ["0000989556", "0000989792"],
  "reference_question": "How did the moisture content specifications change between the 1985 and 1987 PHOENIX cigarette specifications?",
  "answer": "The moisture content decreased from 13.5% in 1985 to 12.8% in 1987, a reduction of 0.7 percentage points.",
  "type": "comparative_reasoning"
}
```

When comparative reasoning spans multiple documents, the relationship between documents should be explicitly categorized as one of the following types:

### Document Relationship Types

- **Chronological**: Time-based relationship (e.g., versions, updates, sequential documents)
  ```json
  {
    "id": "qa_comparative_002",
    "supporting_documents": ["0000989556", "0000989792"],
    "reference_question": "How did the cigarette specifications evolve from 1985 to 1987?",
    "answer": "The moisture content decreased from 13.5% to 12.8%, and the tipping paper substance changed from 36 gm/m² to 32 gm/m².",
    "type": "comparative_reasoning",
    "document_relationship_type": "chronological"
  }
  ```

- **Complementary**: Different aspects of same entity or process (e.g., specification and implementation)
  ```json
  {
    "id": "qa_comparative_003",
    "supporting_documents": ["0000989556", "0001123541"],
    "reference_question": "How do the manufacturing specifications compare to the marketing strategy for the PHOENIX brand?",
    "answer": "The specifications focus on physical characteristics like filter length and pressure drop, while the marketing strategy emphasizes the 'premium quality' derived from these technical attributes.",
    "type": "comparative_reasoning",
    "document_relationship_type": "complementary"
  }
  ```

- **Contradictory**: Documents with conflicting information (e.g., discrepancies between forms)
  ```json
  {
    "id": "qa_comparative_004",
    "supporting_documents": ["0000989556", "0000990274"],
    "reference_question": "What discrepancies exist between the product specification and the actual order?",
    "answer": "The specification calls for a filter length of 20mm, but the order requests a modified filter length of 21mm.",
    "type": "comparative_reasoning",
    "document_relationship_type": "contradictory"
  }
  ```

- **Prerequisite**: One document needed to understand another (e.g., reference documentation)
  ```json
  {
    "id": "qa_comparative_005",
    "supporting_documents": ["0000989556", "0001463448"],
    "reference_question": "Using the terminology defined in the specifications document, explain the production requirements in the manufacturing order.",
    "answer": "The manufacturing order requires 'encapsulated pressure drop' to match 120mm as defined in the specifications document, which refers to the resistance to airflow measured with the filter section fully sealed.",
    "type": "comparative_reasoning",
    "document_relationship_type": "prerequisite"
  }
  ```

## 12. Counterfactual Reasoning
Reasoning about hypothetical scenarios or "what if" questions based on document information.

**Example:**
```json
{
  "id": "qa_counterfactual_001",
  "supporting_documents": ["0000989556"],
  "reference_question": "If the tobacco content in the PHOENIX cigarette were increased by 10%, what would the new cigarette weight be?",
  "answer": "1048.9 mg",
  "type": "counterfactual_reasoning"
}
```

## 13. Visual Reasoning
Questions requiring understanding of visual elements, layout relationships, or appearance that may not be fully captured in text.

**Example:**
```json
{
  "id": "qa_visual_001",
  "supporting_documents": ["87147607"],
  "reference_question": "Is the company logo positioned above or below the document title in the form letter?",
  "answer": "Above",
  "type": "visual_reasoning"
}
``` 