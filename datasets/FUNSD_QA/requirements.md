# FUNSD_QA Dataset Requirements

This document outlines the key requirements for creating a comprehensive and useful question-answer dataset based on FUNSD.

## Core Requirements

1. **Document Type Diversity**
   - Include QA pairs from all form types present in FUNSD (invoices, orders, letters, reports, etc.)
   - Ensure balanced representation of different document categories
   - Consider document complexity in selection (simple forms vs. complex multi-section documents)

2. **Document Type Balance**
   - Include questions across all seven document categories (see document_types.md)
   - Ensure representation of Transactional, Contractual, Correspondence, Administrative, Financial, HR, and Regulatory documents
   - Create type-specific questions that test understanding of each document type's unique characteristics
   - Include cross-type questions requiring understanding relationships between different document types
   - Consider domain knowledge questions that test understanding of field-specific terminology
   - Pay attention to type-specific visual elements and layouts in questions

3. **Question Type Balance**
   - Each document should have questions representing multiple types (see qa_types.md)
   - Maintain a balanced distribution of question types across the entire dataset
   - Ensure each question type is represented across different document categories

4. **Difficulty Level Distribution**
   - Include a mix of easy, medium, and hard questions for each document
   - Define difficulty based on factors like:
     - Number of reasoning steps required
     - Complexity of document layout
     - Ambiguity of information
     - Need for external knowledge
   - Aim for approximately 40% easy, 40% medium, 20% hard distribution

5. **Document-Specific Relevance**
   - Questions should be tailored to each document's specific content and purpose
   - Focus on information that would be naturally sought from that document type
   - Include domain-specific questions where appropriate

6. **Domain Variety**
   - Cover business-related questions (costs, dates, parties involved)
   - Include administrative questions (processing steps, approvals, references)
   - Add technical questions for documents with technical content
   - Consider industry-specific questions where applicable

7. **Linguistic Diversity**
   - Vary question phrasing and complexity
   - Include both direct and indirect questions
   - Use a range of question words (what, when, where, how, why, etc.)
   - Avoid redundant question patterns

8. **Answer Variability**
   - Include answers of different types (text, numbers, dates, yes/no)
   - Vary answer length (single words, phrases, sentences)
   - Ensure some answers require combining multiple pieces of information

9. **Contextual Appropriateness**
   - All questions should be answerable from the document content
   - Questions should reflect real-world information needs for each document type
   - Include questions that test understanding of document structure and semantics

10. **Evaluation Suitability**
    - QA pairs should effectively test capabilities of RAG and KAG systems
    - Questions should assess both retrieval accuracy and reasoning capabilities
    - Include questions that evaluate layout understanding

11. **RAG-Friendly Questions**
    - Use a hybrid approach with both reference and user-facing questions
    - Reference questions: Clear, concise versions for evaluation scoring
    - User questions: Include sufficient document context to enable effective retrieval
    - Ensure user questions contain enough specificity (document type, entity names, etc.) for accurate retrieval in large collections
    - Design user questions to reflect realistic search queries while maintaining answer validity

12. **Multi-Document Question Coverage**
    - Include a meaningful proportion of questions requiring information from multiple documents
    - Represent all document relationship types: chronological, complementary, contradictory, and prerequisite
    - Vary information synthesis complexity levels from low to high
    - Ensure multi-document questions span different domains and document types
    - Document relationship types should be explicitly defined:
      - **Chronological**: Time-based relationship (e.g., versions, updates, sequential documents)
      - **Complementary**: Different aspects of same entity or process (e.g., specification and implementation)
      - **Contradictory**: Documents with conflicting information (e.g., discrepancies between forms)
      - **Prerequisite**: One document needed to understand another (e.g., reference documentation)

13. **Quality Control**
    - All QA pairs should be manually verified for accuracy
    - Answers should be unambiguous and directly verifiable from the document
    - Document IDs and references should be correctly linked
    - Metadata should be complete and accurate 