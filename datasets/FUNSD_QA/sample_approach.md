# Sample Approach for Creating FUNSD_QA Pairs

This document outlines a systematic approach for creating QA pairs from diverse FUNSD documents and provides examples from different document types.

## Step-by-Step Approach

1. **Document Selection**
   - Choose 3-5 documents of different types from the training set
   - Select documents with varying complexity and content
   - Prioritize documents with clear, readable content
   - Ensure representation across document categories (see document_types.md)
   - Include Transactional, Contractual, Correspondence, Administrative, Financial, HR, and Regulatory documents

2. **Document Analysis**
   - Identify the document type and purpose
   - Note key sections, fields, and information types
   - Map the document structure (headers, tables, form fields)
   - Identify relationships between different parts of the document
   - Identify domain-specific terminology and conventions
   - Note unique visual elements and layouts specific to the document type

3. **Question Generation Strategy**
   - For each document, create at least:
     - 2-3 simple extraction questions
     - 1-2 relationship questions
     - 1 numerical reasoning question
     - 1 layout understanding question
     - 1 verification question
     - 1 multi-hop reasoning question
   - Create type-specific questions that test understanding of each document type's unique characteristics
   - Include cross-type questions requiring understanding relationships between different document types
   - Add domain knowledge questions that test understanding of field-specific terminology
   - Include questions about visual elements specific to the document type

4. **Question Diversity**
   - Vary question formulation and complexity
   - Cover different parts of the document
   - Include questions about document structure
   - Add questions about document-specific features
   - Balance question types across all document categories

5. **RAG-Friendly Question Formulation**
   - Create two versions of each question:
     - **reference_question**: Clean, concise version for evaluation scoring
     - **user_question**: Version with document context for RAG retrieval
   - Add sufficient context to user questions (document type, entity names, dates)
   - Maintain natural question phrasing to reflect realistic queries
   - Example:
     - Reference: "What is the invoice number?"
     - User: "What is the invoice number for the XYZ Corp order from October 1994?"

6. **Multi-Document Question Creation**
   - Identify documents with natural relationships
   - Create questions requiring information from multiple documents
   - Classify according to relationship type (chronological, complementary, contradictory, prerequisite)
   - Assign information synthesis complexity (low, medium, high)
   - Ensure clear reasoning paths across documents
   - Consider the specific relationship type when formulating questions:
     - **Chronological**: Time-based relationships between documents
       - Example: How did specifications change between versions?
       - Example: What steps occurred between initial request and final approval?
     - **Complementary**: Documents providing different aspects of the same entity/process
       - Example: How does the marketing plan align with the budget allocation?
       - Example: What additional details does document B provide about the project in document A?
     - **Contradictory**: Documents with conflicting information
       - Example: What discrepancies exist between the initial order and the invoice?
       - Example: How do the reported metrics differ between documents?
     - **Prerequisite**: One document needed to understand another
       - Example: Using the definitions in document A, explain the terms in document B
       - Example: Based on the policy guidelines, is the procedure in compliance?

7. **Quality Verification**
   - Ensure questions are answerable from the document
   - Verify answer accuracy
   - Check for ambiguity
   - Review difficulty classification
   - Test if user questions contain enough context for retrieval

## Distribution Recommendations

For a well-balanced dataset, aim for these specific distributions:

### Document Type Distribution
- **Transactional Documents**: 20-25% of total questions
  - Invoices: 7-8%
  - Purchase Orders: 5-6%
  - Receipts: 4-5%
  - Other: 4-6%
- **Contractual Documents**: 15-20% of total questions
  - Agreements: 5-7%
  - Product Specifications: 5-7%
  - Other: 5-6%
- **Correspondence**: 15-20% of total questions
  - Business Letters: 8-10%
  - Form Letters: 4-5%
  - Memos: 3-5%
- **Administrative Forms**: 15-20% of total questions
  - Applications: 7-8%
  - Registration Forms: 4-5%
  - Other: 4-7%
- **Financial Documents**: 10-15% of total questions
- **Human Resources Documents**: 5-10% of total questions
- **Regulatory Documents**: 5-10% of total questions

### Question Type Distribution
- **Extraction**: 20%
- **Entity Detection**: 10%
- **Relationship**: 10%
- **Numerical Reasoning**: 10%
- **Temporal Reasoning**: 5-10%
- **Layout Understanding**: 10%
- **Multi-hop Reasoning**: 10%
- **Classification**: 5%
- **Verification**: 5-10%
- **Summarization**: 5%
- **Comparative Reasoning**: 5%
- **Counterfactual Reasoning**: 5%
- **Visual Reasoning**: 5%

### Difficulty Distribution
- **Easy**: 40%
- **Medium**: 40%
- **Hard**: 20%

### Multi-Document Questions
- Make up 15-20% of the total dataset
- **Relationship Types**:
  - Chronological: 40%
  - Complementary: 30%
  - Contradictory: 20%
  - Prerequisite: 10%
- **Synthesis Complexity**:
  - Low: 30%
  - Medium: 50%
  - High: 20%

## Document Type Coverage Examples

To ensure balanced representation, here are examples of questions for different document types:

### 1. Transactional Document (Invoice)

```json
[
  {
    "id": "qa_extraction_002",
    "reference_question": "What is the invoice number?",
    "user_question": "What is the invoice number on the XYZ Corp order from October 7, 1994?",
    "answer": "49867",
    "type": "extraction"
  },
  {
    "id": "qa_numerical_002",
    "reference_question": "What is the tax rate applied to this invoice?",
    "user_question": "What is the tax rate applied to invoice #49867 from October 1994?",
    "answer": "8.25%",
    "type": "numerical_reasoning"
  }
]
```

### 2. Contractual Document (Product Specification)

```json
[
  {
    "id": "qa_extraction_001",
    "reference_question": "What is the brand name listed in the product specification?",
    "user_question": "What is the brand name listed in the B.A.T. CYPRUS cigarette product specification from 1985?",
    "answer": "PHOENIX",
    "type": "extraction"
  },
  {
    "id": "qa_relationship_001",
    "reference_question": "What company manufactures the PHOENIX brand?",
    "user_question": "According to the 1985 cigarette specification, what company manufactures the PHOENIX brand?",
    "answer": "B.A.T. CYPRUS",
    "type": "relationship"
  }
]
```

### 3. Correspondence (Form Letter)

```json
[
  {
    "id": "qa_extraction_003",
    "reference_question": "Who is the letter addressed to?",
    "user_question": "Who is the ABC Corporation form letter from February 1994 addressed to?",
    "answer": "John Smith",
    "type": "extraction"
  },
  {
    "id": "qa_layout_001",
    "reference_question": "What appears in the top right corner of the letter?",
    "user_question": "What appears in the top right corner of the ABC Corporation form letter?",
    "answer": "Company Logo",
    "type": "layout_understanding"
  }
]
```

### 4. Administrative Form (Application)

```json
[
  {
    "id": "qa_entity_001",
    "reference_question": "What personal information fields are required on this application?",
    "user_question": "What personal information fields are required on the XYZ membership application form?",
    "answer": "Name, Address, Phone Number, Date of Birth",
    "type": "entity_detection"
  },
  {
    "id": "qa_verification_001",
    "reference_question": "Does this application require a witness signature?",
    "user_question": "Does the XYZ membership application form from 1994 require a witness signature?",
    "answer": "Yes",
    "type": "verification"
  }
]
```

## Cross-Document Question Examples

```json
[
  {
    "id": "qa_comparative_001",
    "reference_question": "How did the order quantity change between the purchase order and the final invoice?",
    "user_question": "How did the XYZ Corp order quantity change between purchase order #PO-7842 and the final invoice #49867 from October 1994?",
    "answer": "Increased from 500 to 750 units",
    "type": "comparative_reasoning",
    "supporting_documents": ["93418723", "82253058_3059"]
  }
]
```

## Implementation Tips

1. **Start Small**
   - Begin with 3-5 diverse documents
   - Create 7-10 questions per document
   - Cover at least 5 different question types per document

2. **Document as You Go**
   - Note challenges or ambiguities encountered
   - Record time spent per document
   - Identify patterns that could be automated

3. **Review and Refine**
   - Have another person review your QA pairs
   - Test with a simple retrieval system if possible
   - Refine questions that are ambiguous or too difficult

4. **Scale Gradually**
   - Apply lessons learned to more documents
   - Maintain consistent quality standards
   - Consider question templates for similar document types

5. **Maintain Balance**
   - Track statistics on question types and difficulty
   - Adjust creation strategy to maintain desired distribution
   - Ensure coverage across document types

6. **Test RAG Retrieval**
   - Verify that user questions contain sufficient context for accurate retrieval
   - Check if similar documents can be distinguished through question phrasing
   - Ensure both reference and user questions lead to the same answer 