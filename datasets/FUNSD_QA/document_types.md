# FUNSD Document Types

This document provides a classification of document types found in the FUNSD dataset to guide the creation of a balanced question-answer dataset with diverse document representation.

## 1. Transactional Documents

Documents related to business transactions and exchanges of goods or services.

- **Invoices**: Bills for products or services sold
- **Purchase Orders**: Formal requests to purchase goods/services
- **Receipts**: Confirmation of payment for goods/services
- **Packing Slips**: Documents listing items included in a shipment
- **Delivery Notes**: Documentation of items delivered
- **Order Forms**: Forms used to place orders for products/services

## 2. Contractual Documents

Documents establishing formal agreements between parties.

- **Agreements**: Formal contracts between parties
- **Terms & Conditions**: Rules governing business relationships
- **Product Specifications**: Detailed product requirements (e.g., cigarette specifications)
- **Service Agreements**: Contracts for ongoing services
- **Warranty Documents**: Guarantees for products or services

## 3. Correspondence

Written communication between individuals or organizations.

- **Business Letters**: Formal communication between organizations
- **Form Letters**: Template-based communication to customers/clients
- **Memos**: Internal business communications
- **Notices**: Formal announcements or alerts
- **Inquiry Letters**: Requests for information

## 4. Administrative Forms

Documents used for organizing, managing, or facilitating organizational processes.

- **Application Forms**: Documents to request services/membership
- **Registration Forms**: Documents to register for events/services
- **Enrollment Forms**: Documents to join programs
- **Survey Forms**: Documents collecting feedback/information
- **Claim Forms**: Documents for submitting claims

## 5. Financial Documents

Documents related to financial transactions, reporting, or status.

- **Financial Statements**: Reports of financial performance
- **Expense Reports**: Documentation of business expenses
- **Balance Sheets**: Summaries of assets, liabilities, and equity
- **Account Statements**: Records of financial transactions
- **Tax Forms**: Documents related to tax reporting or payment

## 6. Human Resources Documents

Documents related to employment and personnel management.

- **Employment Applications**: Forms to apply for jobs
- **Performance Reviews**: Assessments of employee performance
- **Benefit Forms**: Documents related to employee benefits
- **Timesheets**: Records of hours worked
- **Personnel Records**: Documentation of employee information

## 7. Regulatory Documents

Documents related to compliance with laws, regulations, or standards.

- **Compliance Forms**: Documents ensuring regulatory adherence
- **Inspection Reports**: Documentation of regulatory inspections
- **Certification Documents**: Proof of compliance with standards
- **Licenses**: Official permissions to conduct activities
- **Permits**: Authorizations to perform specific actions

## Document Representation Guidelines

When creating QA pairs for the FUNSD_QA dataset:

1. **Balanced Representation**: Include questions from documents across all categories
2. **Type-Specific Questions**: Create questions that test understanding of each document type's unique characteristics
3. **Cross-Type Questions**: Include questions requiring understanding relationships between different document types
4. **Domain Knowledge**: Consider questions that test understanding of domain-specific terminology and conventions
5. **Visual Elements**: Pay attention to type-specific visual elements and layouts

## Document Type Distribution

For a well-balanced dataset, aim for roughly equal representation across these categories, or adjust based on the actual distribution in the FUNSD dataset. 