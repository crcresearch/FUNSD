# Question-Answer Pair Additional Fields

This document describes the additional fields that can be included in each question-answer pair in the FUNSD_QA dataset.

## Required Fields

### id
A unique identifier for the QA pair.
- **Format:** String, preferably with a prefix indicating the type (e.g., "qa_extraction_001")
- **Example:** "qa_001"

### reference_question
The clean, focused question for evaluation scoring.
- **Format:** String
- **Example:** "What is the brand name listed in the product specification?"

### user_question
The question with document context for RAG retrieval.
- **Format:** String
- **Example:** "What is the brand name listed in the B.A.T. CYPRUS cigarette product specification from 1985?"

### answer
The answer to the question.
- **Format:** String
- **Example:** "PHOENIX"

### type
The category of question-answer pair (see qa_types.md).
- **Format:** String, one of the predefined types
- **Example:** "extraction"

### supporting_documents
List of document IDs needed to answer the question.
- **Format:** Array of strings
- **Example:** ["0000989556"]

## Optional Fields

### difficulty
Indicates how challenging the question is to answer.
- **Format:** String, one of ["easy", "medium", "hard"]
- **Example:** "medium"

### context
The relevant text surrounding the answer, providing context.
- **Format:** String
- **Example:** "Brand: PHOENIX\nStyle: KS8 - KS"

### section
The document section where the answer is found.
- **Format:** String
- **Example:** "PRODUCT SPECIFICATION"

### supporting_sections
Specific sections within documents needed for the answer.
- **Format:** Array of objects with document_id and section fields
- **Example:** [{"document_id": "0000989556", "section": "PRODUCT SPECIFICATION"}]

### reasoning_path
Step-by-step reasoning process to arrive at the answer.
- **Format:** Array of strings
- **Example:** ["Identify manufacturing location (NICOSIA)", "Find tipping paper specs", "Extract substance value"]

### bbox
Bounding box coordinates for visualizing the answer location in the document image.
- **Format:** Array of four integers [left, top, right, bottom]
- **Example:** [100, 200, 300, 250]

### entity_ids
References to original FUNSD entity IDs related to this QA pair.
- **Format:** Array of strings
- **Example:** ["q_123", "a_456"]

### requires_reasoning
Indicates whether inference beyond direct extraction is needed.
- **Format:** Boolean
- **Example:** true

### document_relationship_type
For multi-document questions, the relationship type between documents.
- **Format:** String, one of ["chronological", "complementary", "contradictory", "prerequisite"]
- **Example:** "chronological"

### information_synthesis_complexity
For multi-document questions, the complexity of synthesizing information.
- **Format:** String, one of ["low", "medium", "high"]
- **Example:** "medium"

### requires_image
Whether answering requires the document image (not just text).
- **Format:** Boolean
- **Example:** true

### visual_elements
Visual elements relevant to answering the question.
- **Format:** Array of strings
- **Example:** ["logo", "signature", "header"]

### generation_method
How the QA pair was created.
- **Format:** String, one of ["manual", "semi_automated", "automated"]
- **Example:** "manual"

### confidence
For automatically generated pairs, the confidence score of the generation.
- **Format:** Float between 0 and 1
- **Example:** 0.95

### verified
Indicates whether the QA pair has been verified by a human.
- **Format:** Boolean
- **Example:** true

## Complete Example

```json
{
  "id": "qa_multihop_001",
  "reference_question": "What is the Tipping Paper substance measurement for the product manufactured in NICOSIA?",
  "user_question": "What is the Tipping Paper substance measurement for the PHOENIX cigarettes manufactured in NICOSIA according to the B.A.T. CYPRUS specification?",
  "answer": "36 gm/m²",
  "type": "multi_hop_reasoning",
  "supporting_documents": ["0000989556"],
  "difficulty": "hard",
  "supporting_sections": [
    {"document_id": "0000989556", "section": "PRODUCT SPECIFICATION"},
    {"document_id": "0000989556", "section": "Tipping and Tipping Application"}
  ],
  "reasoning_path": [
    "Identify the manufacturing location in the PRODUCT SPECIFICATION section (NICOSIA)",
    "Find the tipping paper specifications in the Tipping and Tipping Application section",
    "Extract the substance measurement value (36 gm/m²)"
  ],
  "context": "Place of Manufacture: NICOSIA\n\n...\n\nSubstance: 36 | gm/m²",
  "section": "Tipping and Tipping Application",
  "bbox": [318, 642, 348, 658],
  "entity_ids": ["entity_42", "entity_87"],
  "requires_reasoning": true,
  "generation_method": "manual",
  "verified": true
}
```

## Multi-Document Example

```json
{
  "id": "qa_comparative_001",
  "reference_question": "How did the moisture content specifications change between the 1985 and 1987 PHOENIX cigarette specifications?",
  "user_question": "What changed in the moisture content specifications between the 1985 and 1987 PHOENIX cigarette documents?",
  "answer": "The moisture content decreased from 13.5% in 1985 to 12.8% in 1987, a reduction of 0.7 percentage points.",
  "type": "comparative_reasoning",
  "supporting_documents": ["0000989556", "0000989792"],
  "difficulty": "medium",
  "supporting_sections": [
    {"document_id": "0000989556", "section": "CIGARETTE MAKING"},
    {"document_id": "0000989792", "section": "PHYSICAL PROPERTIES"}
  ],
  "reasoning_path": [
    "Locate moisture content in the 1985 document (13.5%)",
    "Find moisture content in the 1987 document (12.8%)",
    "Calculate the difference (0.7 percentage points)"
  ],
  "document_relationship_type": "chronological",
  "information_synthesis_complexity": "low",
  "requires_reasoning": true,
  "generation_method": "manual",
  "verified": true
}
``` 