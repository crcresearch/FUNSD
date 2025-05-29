# FUNSD QA Dataset Evaluation

## Dataset Composition
- **Total Documents**: 149 documents with QA pairs
- **Document Types Distribution**:
  - Correspondence (51 documents, 34%)
  - Administrative (39 documents, 26%)
  - Transactional (19 documents, 13%)
  - Financial (13 documents, 9%)
  - Contractual (13 documents, 9%)
  - Regulatory (7 documents, 5%)
  - HR (7 documents, 5%)

## QA Pairs Characteristics
- **Average QA Pairs per Document**: ~25-30 pairs per document
- **Question Types Distribution** (based on samples):
  - Entity Detection: ~25%
  - Verification: ~16% 
  - Multi-hop Reasoning: ~11%
  - Temporal Reasoning: ~9%
  - Numerical Reasoning: ~8%
  - Extraction: ~8%
  - Relationship: ~7%
  - Layout Understanding: ~5%
  - Classification: ~5%
  - Comparative Reasoning: ~4%
  - Summarization: ~2%

- **Difficulty Levels**:
  - Medium: ~48%
  - Easy: ~41%
  - Hard: ~11%

- **Reasoning Requirements**:
  - Requires reasoning: ~72%
  - Simple extraction (no reasoning): ~28%

- **Verification Status**:
  - All QA pairs are marked as verified

## Quality Assessment
The dataset demonstrates several strengths:

1. **Diverse Document Types**: Covers a wide range of administrative, financial, and correspondence documents
2. **Comprehensive Question Types**: Includes questions requiring different cognitive skills from simple extraction to complex reasoning
3. **Balanced Difficulty Levels**: Good distribution across easy, medium, and hard questions
4. **High Reasoning Proportion**: ~72% of questions require reasoning beyond simple extraction
5. **Structured Format**: Well-organized JSON format with consistent fields
6. **Detailed Context**: Each QA pair includes relevant context from the document
7. **Reasoning Paths**: Complex questions include explicit reasoning paths
8. **Verification**: All QA pairs are verified for accuracy

## Evaluation Metrics & Recommendations

For evaluating model performance on this dataset, consider:

1. **Overall Accuracy**: Percentage of correctly answered questions
2. **Question Type Performance**: Breakdown of accuracy by question type
3. **Difficulty Level Analysis**: Performance across easy/medium/hard questions
4. **Reasoning vs. Extraction**: Compare performance on questions requiring reasoning vs. simple extraction
5. **Document Type Analysis**: Performance across different document categories

For comprehensive evaluation, I recommend:

1. **Benchmark Testing**: Test several LLMs to establish baseline performance
2. **Human Evaluation**: Have human annotators evaluate a sample of model answers
3. **Error Analysis**: Categorize errors to identify systematic weaknesses
4. **Reasoning Validation**: For complex questions, evaluate if models follow similar reasoning paths
5. **Cross-Document Evaluation**: Test if models can handle cross-document questions by adding some multi-document questions

## Sample QA Pair Structure

```json
{
  "id": "qa_multi_hop_001",
  "reference_question": "What is the location of the reporter and the information source?",
  "user_question": "Based on the document, what is the geographical relationship between the reporter's location and the source of information?",
  "answer": "Both are located in Ohio; the reporter (R. E. Klein) is in Cleveland, OH while the information source (Best Cigarette Co.) is in Mentor, OH",
  "type": "multi_hop_reasoning",
  "difficulty": "hard",
  "supporting_documents": ["93455715"],
  "section": "Multiple Sections",
  "context": "REPORTED BY: R. E. Klein, Regional Sales Manager, Cleveland, OH\nSOURCE OF INFORMATION: Best Cigarette Co., Mentor, OH",
  "requires_reasoning": true,
  "reasoning_path": [
    "The reporter is identified as R. E. Klein, Regional Sales Manager, Cleveland, OH",
    "The source of information is Best Cigarette Co., Mentor, OH",
    "Both locations are in Ohio (OH)",
    "Cleveland and Mentor are different cities within the same state",
    "Therefore, both the reporter and the information source are located in Ohio, but in different cities"
  ],
  "generation_method": "manual",
  "verified": true
}
```

## Conclusion

The FUNSD QA dataset provides a robust resource for evaluating document understanding capabilities. Its diverse question types, balanced difficulty levels, and high proportion of reasoning-based questions make it particularly valuable for assessing advanced language models. The dataset's strength lies in its comprehensive coverage of various document types and reasoning complexities, providing a solid foundation for benchmarking document AI systems.

The careful attention to verification and the inclusion of reasoning paths for complex questions further enhance its utility for research and development in document understanding.

_Evaluation Date: June 14, 2023_ 