# FUNSD QA Dataset

## Overview
This dataset consists of 149 processed documents from the FUNSD (Form Understanding in Noisy Scanned Documents) dataset, enriched with comprehensive question-answer pairs for document understanding tasks.

Each document has been annotated with approximately 25-30 QA pairs covering various question types and difficulty levels, designed to test different aspects of document comprehension. In total, the dataset contains approximately 3,700+ QA pairs across all documents.

## Dataset Structure

### Directory Organization
- `training/` - Contains all QA pairs JSON files (named as `qa_pairs_[document_id].json`)
- `training/document_metadata.json` - Metadata for all training documents including paths and document types
- `dataset_evaluation.md` - Comprehensive evaluation of the dataset characteristics
- `requirements.md` - Key requirements for creating a comprehensive and useful question-answer dataset based on FUNSD
- `document_types.md` - Classification of document types found in the FUNSD dataset
- `qa_types.md` - Description of the different types of question-answer pairs in the dataset
- `schema.py` - Pydantic models and enums defining the data structures used in the dataset

### QA Pair Format
Each QA pair is structured as a JSON object with the following fields:
- `id`: Unique identifier for the QA pair
- `reference_question`: The canonical form of the question
- `user_question`: The question as it would be asked by a user
- `answer`: The correct answer
- `type`: The type of reasoning required (e.g., entity_detection, multi_hop_reasoning)
- `difficulty`: The difficulty level (easy, medium, hard)
- `supporting_documents`: Document IDs needed to answer the question
- `section`: The relevant section of the document
- `context`: The specific text from the document needed to answer the question
- `requires_reasoning`: Boolean indicating if reasoning beyond simple extraction is required
- `reasoning_path` (optional): Step-by-step reasoning path for complex questions
- `generation_method`: How the QA pair was generated
- `verified`: Whether the QA pair has been verified

## Document Types
The dataset includes diverse document types:
- Correspondence (51 documents, 34%)
- Administrative (39 documents, 26%)
- Transactional (19 documents, 13%)
- Financial (13 documents, 9%)
- Contractual (13 documents, 9%)
- Regulatory (7 documents, 5%)
- HR (7 documents, 5%)

## Question Types
The dataset includes a variety of question types to test different reasoning capabilities:
- Entity Detection (25%): Identify specific entities mentioned in documents
- Verification (16%): Verify if a statement is true or false based on document content
- Multi-hop Reasoning (11%): Connect information from different parts of a document
- Temporal Reasoning (9%): Reason about dates, time periods, and sequences
- Numerical Reasoning (8%): Perform calculations or numerical comparisons
- Extraction (8%): Extract specific information from document text
- Relationship (7%): Identify relationships between entities or concepts
- Layout Understanding (5%): Understand document structure and layout
- Classification (5%): Classify documents or elements within documents
- Comparative Reasoning (4%): Compare different elements or attributes
- Summarization (2%): Summarize document content or sections

## Getting Started
To use this dataset for evaluation or fine-tuning:

1. Load a QA pairs file:
```python
import json

# Load QA pairs for a specific document
with open('datasets/FUNSD_QA/training/qa_pairs_93455715.json', 'r') as f:
    qa_pairs = json.load(f)

# Example: Print the first question and answer
print(f"Question: {qa_pairs[0]['user_question']}")
print(f"Answer: {qa_pairs[0]['answer']}")
print(f"Type: {qa_pairs[0]['type']}")
print(f"Difficulty: {qa_pairs[0]['difficulty']}")
```

2. Group questions by type or difficulty:
```python
# Group questions by type
question_types = {}
for qa in qa_pairs:
    q_type = qa['type']
    if q_type not in question_types:
        question_types[q_type] = []
    question_types[q_type].append(qa)

# Print count of each type
for q_type, questions in question_types.items():
    print(f"{q_type}: {len(questions)} questions")
```

## Evaluation Methodology
When evaluating models on this dataset, we recommend:

1. **Stratified Evaluation**: Report performance across different question types and difficulty levels
2. **Reasoning Assessment**: Separately evaluate performance on questions requiring reasoning vs. simple extraction
3. **Document Type Analysis**: Analyze performance across different document types
4. **Exact Match vs. Semantic Accuracy**: Consider both exact string matches and semantic correctness
5. **Error Analysis**: Categorize errors to identify systematic weaknesses in models

See the [dataset evaluation document](dataset_evaluation.md) for detailed evaluation metrics and recommendations.

## Usage
This dataset is designed for evaluating document understanding capabilities of AI models, particularly for:
- Information extraction
- Question answering
- Complex reasoning over documents
- Layout understanding
- Temporal and numerical reasoning

## Dataset Creation Process
The QA pairs were created following this methodology:
1. Document selection from the FUNSD dataset
2. Analysis of document content and structure
3. Creation of diverse question types covering different aspects of understanding
4. Ensuring balanced distribution of difficulty levels
5. Adding reasoning paths for complex questions
6. Verification of all QA pairs for accuracy and consistency

## Limitations
- The dataset focuses primarily on forms and administrative documents, which may limit generalization to other document types
- Questions are limited to information contained within each document (no external knowledge required)
- While efforts were made to create diverse questions, certain document types or question categories may be overrepresented
- All documents are in English, limiting cross-lingual evaluation

## Citation
If you use this dataset in your research or applications, please cite the original FUNSD dataset:

```
@article{jaume2019funsd,
  title={FUNSD: A Dataset for Form Understanding in Noisy Scanned Documents},
  author={Jaume, Guillaume and Ekenel, Hazim Kemal and Thiran, Jean-Philippe},
  journal={2019 International Conference on Document Analysis and Recognition Workshops (ICDARW)},
  volume={2},
  pages={1--6},
  year={2019},
  organization={IEEE}
}
```

## Acknowledgements
Special thanks to the creators of the original FUNSD dataset and all contributors who helped in creating and annotating the QA pairs. 