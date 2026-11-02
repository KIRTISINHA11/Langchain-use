

# Document 1

Metadata:
```json
{
  "source": "C:\\Users\\Admin\\Agentic AI Projects\\AI\\RAG\\Langchain-use\\data\\Client_Contracts_Policies_and_Incident_Records.pdf",
  "page_number": 1,
  "content_type": "page_text",
  "character_count": 1316
}
```

Content:
Complex RAG Parsing Sample - synthetic document
Page 1
Complex Document for RAG Parsing Tests
Synthetic 15-page PDF with paragraphs, simple and complex tables, diagrams, scanned-form style image, metadata
examples, and production RAG edge cases.
Story Line
Three client teams - Arka Finance, BlueLeaf Retail, and CityRide Mobility - are migrating contracts, policies, support records,
and operational reports into a single RAG platform. Each team has different document types, access rules, and parsing
challenges. The RAG system must answer questions with citations while ensuring that one client never sees another clients
data.
This PDF is intentionally designed to test document loaders, PDF parsers, OCR workflows, table extraction, chunking
strategies, metadata preservation, and source citation quality.
Key statement: RAG does not train the model. RAG gives the model the right context before answering.
Section
Parsing challenge
Why it matters for RAG
Contracts
Dense legal text, clause numbers, cross
references
Need section-aware chunks and citations
Tables
Merged headers, numeric columns,
footnotes
Need row/column preservation
Images
Architecture diagram, heatmap, scanned
form
Need OCR or multimodal extraction
Multi-tenant metadata
client_id, document_id,
contract_group_id
Need access-safe retrieval

---


# Document 2

Metadata:
```json
{
  "source": "C:\\Users\\Admin\\Agentic AI Projects\\AI\\RAG\\Langchain-use\\data\\Client_Contracts_Policies_and_Incident_Records.pdf",
  "page_number": 2,
  "content_type": "page_text",
  "character_count": 1226
}
```

Content:
Complex RAG Parsing Sample - synthetic document
Page 2
1. Business Scenario
The platform team is building a document intelligence layer for contract operations. Legal users need answers such as: Which
contracts renew automatically? Which agreements have a 60-day termination notice? Which documents mention data
residency in India? These questions require retrieval across multiple document types and sometimes across multiple related
documents of a single client.
Support teams also want answers from SOPs, markdown runbooks, HTML exports, chat transcripts, and CSV logs. A single
parser is not enough because the corpus contains born-digital PDFs, scanned forms, HTML, markdown, and spreadsheet-like
tables.
Client
Main document family
Risk
Primary users
Typical question
Arka Finance
MSA, audit addendum, DPA
High
Legal and compliance
What audit rights exist in the DPA?
BlueLeaf Retail
MSA, pricing, support SLA
Medium
Procurement
Which clause controls renewal
pricing?
CityRide Mobility
Ops reports, incident logs,
SOPs
Medium
Operations
Which depot had repeated battery
incidents?
Caption: Ownership map showing how client admins, legal teams, audit teams, document storage, vector storage, and the RAG service interact.

---


# Document 3

Metadata:
```json
{
  "source": "C:\\Users\\Admin\\Agentic AI Projects\\AI\\RAG\\Langchain-use\\data\\Client_Contracts_Policies_and_Incident_Records.pdf",
  "page_number": 3,
  "content_type": "page_text",
  "character_count": 1395
}
```

Content:
Complex RAG Parsing Sample - synthetic document
Page 3
2. Raw Data Inventory
The ingestion team receives files from multiple sources. Some files are clean and digital; others contain scanned pages,
rotated tables, missing metadata, embedded images, or formula-generated values. The inventory below intentionally includes
different formats and extraction expectations.
Asset ID
Client
Format
Pages/Rows
Expected extraction
Notes
ARK-MSA-001
Arka Finance
PDF
32 pages
Clauses, tables, signatures
Born-digital text with footer
references
ARK-DPA-002
Arka Finance
DOCX
18 pages
Headings, lists, tables
Track changes removed
before ingestion
BLR-PRICE-00
3
BlueLeaf Retail
XLSX
12 sheets
Rate cards, discounts
Merged cells and formulas
BLR-SLA-004
BlueLeaf Retail
PDF
9 pages
SLA table, escalation matrix
Table crosses page boundary
CRM-OPS-005
CityRide Mobility
CSV
48,200 rows
Incident records
Needs column type
normalization
CRM-FORM-00
6
CityRide Mobility
Scanned PDF
4 pages
OCR fields, checkbox
Low contrast and slight
rotation
KB-RUN-007
Shared
Markdown
14 files
Runbook sections
Good for heading-based
chunks
WEB-FAQ-008
Shared
HTML
23 pages
FAQ content, links
Needs boilerplate removal
Parsing difficulty increases when a document combines multiple layouts: paragraph text, tables, images, and notes. Good
parsers preserve structure; weak parsers flatten everything into a noisy text stream.

---


# Document 4

Metadata:
```json
{
  "source": "C:\\Users\\Admin\\Agentic AI Projects\\AI\\RAG\\Langchain-use\\data\\Client_Contracts_Policies_and_Incident_Records.pdf",
  "page_number": 4,
  "content_type": "page_text",
  "character_count": 2146
}
```

Content:
Complex RAG Parsing Sample - synthetic document
Page 4
3. Contract Excerpt: Dense Legal Text
Clause 7.2 - Confidential Information. The Receiving Party shall protect Confidential Information using at least the same
degree of care that it uses to protect its own confidential materials, but in no event less than reasonable care. Confidential
Information includes technical documents, pricing schedules, user lists, API keys, operational procedures, security reports,
incident response notes, product roadmaps, and any derived analysis prepared by the Receiving Party.
Clause 7.3 - Exclusions. Confidential Information does not include information that is publicly available without breach,
independently developed without reference to the Disclosing Party material, received lawfully from a third party, or approved
for release in writing. The burden of proving an exclusion remains with the Receiving Party.
Clause 9.1 - Data Residency. If the Statement of Work identifies a specific processing region, the service provider shall
process production records only within that region unless the client approves a transfer in writing. Disaster recovery replicas
may be stored in a secondary region if encryption at rest and access logging are enabled.
Clause 11.4 - Termination Assistance. Upon termination, the provider shall make client data available for export for a period
of thirty days. After the export period, the provider may delete production data according to the deletion schedule unless a
legal hold applies.
Clause
Short name
Owner
Trigger
Required action
Citation hint
7.2
Confidentiality
Receiving Party
Receipt of confidential
material
Protect information with reasonable care
and equivalent internal controls
Page 4, clause
7.2
9.1
Data residency
Service Provider
SOW specifies region
Process production records only in
approved region
Page 4, clause
9.1
11.4
Termination
assistance
Service Provider
Agreement
termination
Provide export window for 30 days
Page 4, clause
11.4
Parser note: clause numbering is important. Chunking should not remove or split clause identifiers because users often
ask questions using clause numbers.

---


# Document 5

Metadata:
```json
{
  "source": "C:\\Users\\Admin\\Agentic AI Projects\\AI\\RAG\\Langchain-use\\data\\Client_Contracts_Policies_and_Incident_Records.pdf",
  "page_number": 5,
  "content_type": "page_text",
  "character_count": 1192
}
```

Content:
Complex RAG Parsing Sample - synthetic document
Page 5
4. Simple Table: Policy Rules
The following table is intentionally simple. It should be correctly extracted by most PDF table parsers. It tests basic row and
column detection, short text values, and numeric values.
Policy Area
Rule
Owner
Review Cycle
Refunds
Refund requests must be raised within 7 days of
purchase.
Customer Support
Quarterly
Data Export
Client admins can request export in CSV or JSON
format.
Platform Ops
Monthly
Access Review
Privileged access must be reviewed every 30 days.
Security
Monthly
Incident Response
Critical incidents require acknowledgement within 30
minutes.
SRE
After each incident
Vendor Review
High-risk vendors require annual risk assessment.
Procurement
Annual
Narrative Around the Table
This table appears between paragraphs, which is common in enterprise documents. A good parser should preserve the
paragraph before the table, the table content, and the paragraph after the table in the correct reading order.
For RAG systems, simple tables are often converted into row-wise text chunks such as: Policy Area: Refunds; Rule: Refund
requests must be raised within 7 days; Owner: Customer Support.

---


# Document 6

Metadata:
```json
{
  "source": "C:\\Users\\Admin\\Agentic AI Projects\\AI\\RAG\\Langchain-use\\data\\Client_Contracts_Policies_and_Incident_Records.pdf",
  "page_number": 6,
  "content_type": "page_text",
  "character_count": 1369
}
```

Content:
Complex RAG Parsing Sample - synthetic document
Page 6
5. Complex Table: SLA, Escalation, and Credits
This table uses long cells and operational footnotes. It is designed to test whether the parser can retain header hierarchy and
map values to the correct columns.
Service Category
Severity
Response Target
Resolution Target
Service Credit
Evidence Required
API Availability
P1 - complete
outage
15 minutes
4 hours
10 percent monthly
fee credit
Monitoring logs and incident
ticket
API Availability
P2 - degraded
performance
30 minutes
8 hours
5 percent monthly fee
credit
Latency dashboard and
affected endpoint list
Data Pipeline
P1 - ingestion
stopped
20 minutes
6 hours
8 percent pipeline fee
credit
Queue depth, failed job IDs,
replay report
Data Pipeline
P3 - delayed
batch
4 hours
Next business day
No automatic credit
Batch ID and SLA exception
note
Support
P2 - urgent
support
1 hour
1 business day
2 percent support fee
credit
Support ticket with timestamps
Footnote A: Service credits are not cumulative across the same service category for the same calendar month. Footnote B: Credits do not apply
when delay is caused by client-side network restrictions, missing credentials, or force majeure events.
Parser note: table footnotes should remain attached to the table. If the footnote is separated, an answer about credits may
become incomplete or misleading.

---


# Document 7

Metadata:
```json
{
  "source": "C:\\Users\\Admin\\Agentic AI Projects\\AI\\RAG\\Langchain-use\\data\\Client_Contracts_Policies_and_Incident_Records.pdf",
  "page_number": 7,
  "content_type": "page_text",
  "character_count": 735
}
```

Content:
Complex RAG Parsing Sample - synthetic document
Page 7
6. Image: RAG Architecture Diagram
The diagram below represents the ingestion and retrieval flow. Some PDF parsers ignore images completely, while others
extract image metadata but not the text inside the image. For production use, image content may require OCR or multimodal
extraction.
Caption: A simplified RAG pipeline showing raw files, parsing, chunking, embeddings, vector database, retriever, LLM, and grounded answer
generation.
Image element
Potential extraction method
Expected output
Box labels
OCR or vision model
Raw Files, Parser, Chunks, Vector DB
Arrows
Layout or vision understanding
Processing order
Caption
Normal PDF text extraction
Description of the diagram

---


# Document 8

Metadata:
```json
{
  "source": "C:\\Users\\Admin\\Agentic AI Projects\\AI\\RAG\\Langchain-use\\data\\Client_Contracts_Policies_and_Incident_Records.pdf",
  "page_number": 8,
  "content_type": "page_text",
  "character_count": 1202
}
```

Content:
Complex RAG Parsing Sample - synthetic document
Page 8
7. Markdown Runbook Excerpt
Markdown files are often easier to parse because headings and code blocks are explicit. However, when markdown is
exported to PDF, the structure may become visual rather than semantic.
# Runbook: Contract Ingestion Failure
## Symptoms
- Upload status remains `processing` for more than 30 minutes.
- Worker logs show repeated timeout errors.
- Vector count does not increase for the affected document.
## Recovery Steps
1. Confirm the object exists in document storage.
2. Re-run parser with `safe_mode=True`.
3. Rebuild chunks with the previous chunking configuration.
4. Compare chunk count with the last successful ingestion.
5. Trigger re-embedding only for changed chunks.
A good parser should preserve code block boundaries and avoid mixing numbered steps with surrounding prose. In RAG,
runbooks are useful because users often ask operational questions that require exact steps.
Runbook field
Value
Parsing expectation
Title
Contract Ingestion Failure
Should become section title metadata
Symptoms
Five bullet items
Should remain as list or separate lines
Recovery Steps
Numbered sequence
Order must be preserved

---


# Document 9

Metadata:
```json
{
  "source": "C:\\Users\\Admin\\Agentic AI Projects\\AI\\RAG\\Langchain-use\\data\\Client_Contracts_Policies_and_Incident_Records.pdf",
  "page_number": 9,
  "content_type": "page_text",
  "character_count": 775
}
```

Content:
Complex RAG Parsing Sample - synthetic document
Page 9
8. Scanned Form and OCR Challenge
This page contains a scanned-form style image. Text inside the form is not normal selectable PDF text. A simple text parser
may miss it entirely. OCR-based systems should extract labels, values, and checkboxes from the image.
Caption: The form includes fields such as Client Name, Contract ID, Effective Date, Renewal Type, Data Region, Reviewer, and a checkbox
approval statement.
Field
Expected OCR value
Validation rule
Client Name
BlueLeaf Retail Pvt Ltd
Must match known client list
Contract ID
BLR-MSA-2026-019
Pattern: client-code + type + year +
sequence
Effective Date
01 Apr 2026
Date parser should normalize to ISO
format
Approval checkbox
Checked
Boolean extraction required

---


# Document 10

Metadata:
```json
{
  "source": "C:\\Users\\Admin\\Agentic AI Projects\\AI\\RAG\\Langchain-use\\data\\Client_Contracts_Policies_and_Incident_Records.pdf",
  "page_number": 10,
  "content_type": "page_text",
  "character_count": 1104
}
```

Content:
Complex RAG Parsing Sample - synthetic document
Page 10
9. Multiple Documents for One Client
BlueLeaf Retail has five related contract documents. If these documents are indexed independently without relationship
metadata, the retriever may miss cross-document context. The platform uses a contract_group_id to connect related
documents.
document_id
document_type
contract_group_id
effective_date
relationship
BLR-MSA-001
Master Service
Agreement
BLR-ACME-2026
2026-04-01
Base commercial agreement
BLR-NDA-002
NDA
BLR-ACME-2026
2026-04-01
Confidentiality terms
BLR-SOW-003
Statement of Work
BLR-ACME-2026
2026-04-15
Project scope and deliverables
BLR-PRICE-004
Pricing Amendment
BLR-ACME-2026
2026-05-01
Updated pricing and discount tiers
BLR-SLA-005
Support SLA
BLR-ACME-2026
2026-05-10
Support response and credits
Example question: What does the BlueLeaf agreement say about termination assistance and pricing changes? A good
retriever may need chunks from the MSA and the Pricing Amendment together.
Relationship metadata allows retrieval across related documents without mixing unrelated client data.

---


# Document 11

Metadata:
```json
{
  "source": "C:\\Users\\Admin\\Agentic AI Projects\\AI\\RAG\\Langchain-use\\data\\Client_Contracts_Policies_and_Incident_Records.pdf",
  "page_number": 11,
  "content_type": "page_text",
  "character_count": 1095
}
```

Content:
Complex RAG Parsing Sample - synthetic document
Page 11
10. Multi-tenant Retrieval and Access Control
In a multi-tenant RAG system, each document, chunk, embedding, and retrieval request should be associated with a tenant
identifier. Client isolation should happen before the LLM receives any context.
Layer
Control
Failure mode if missing
Authentication
Identify user and organization
Unknown user may access application
Authorization
Map user to client_id and role
User may retrieve another clients documents
Vector retrieval
Filter by client_id or namespace
Retriever may return unauthorized chunks
Prompt construction
Send only allowed context
LLM may see sensitive data
Audit logging
Record query, source chunks, user_id
No traceability during incident review
Correct flow: authenticate user, get client_id from backend, retrieve only matching chunks, build prompt with authorized
context, return answer with citations.
Wrong flow: retrieve from all clients and tell the model to ignore unauthorized content. This is unsafe because the LLM should
not be used as the access-control boundary.

---


# Document 12

Metadata:
```json
{
  "source": "C:\\Users\\Admin\\Agentic AI Projects\\AI\\RAG\\Langchain-use\\data\\Client_Contracts_Policies_and_Incident_Records.pdf",
  "page_number": 12,
  "content_type": "page_text",
  "character_count": 788
}
```

Content:
Complex RAG Parsing Sample - synthetic document
Page 12
11. Analytics Image: Retention Heatmap
The heatmap below simulates viewership retention by time slot. A parser that ignores chart images will miss useful business
context. OCR can extract axis labels and numbers, but chart understanding may require a vision model.
Observation
Supporting value
Scheduling implication
Prime Friday performs best
93 retention score
Place premium content in Friday late/prime slots
Early week late slots
underperform
10 to 21 score range
Avoid launching new series in weak slots
Evening improves midweek
77 on Wednesday evening
Use midweek evening for discovery content
For RAG, chart captions should be indexed. If chart values are critical, extract them into structured metadata or a
companion table.

---


# Document 13

Metadata:
```json
{
  "source": "C:\\Users\\Admin\\Agentic AI Projects\\AI\\RAG\\Langchain-use\\data\\Client_Contracts_Policies_and_Incident_Records.pdf",
  "page_number": 13,
  "content_type": "page_text",
  "character_count": 975
}
```

Content:
Complex RAG Parsing Sample - synthetic document
Page 13
12. Evaluation Dataset
A RAG system should be evaluated separately for retrieval quality and answer quality. This page includes a miniature
evaluation set with expected source references. It is useful for testing whether citations point to the correct section.
Test ID
Question
Expected source
Expected answer element
Failure signal
Q-001
What is the refund window?
Policy Rules table
7 days
Answer says 30 days
Q-002
Which clause covers data
residency?
Clause 9.1
Approved processing region
No clause citation
Q-003
What is P1 API response target?
SLA table
15 minutes
Wrong severity row
Q-004
Which documents belong to
BLR-ACME-2026?
Relationship table
Five related documents
Only one document
returned
Q-005
Who owns access review?
Policy Rules table
Security
Owner missing
Evaluation should include adversarial questions, unrelated questions, and questions that require multi-hop retrieval across
related documents.

---


# Document 14

Metadata:
```json
{
  "source": "C:\\Users\\Admin\\Agentic AI Projects\\AI\\RAG\\Langchain-use\\data\\Client_Contracts_Policies_and_Incident_Records.pdf",
  "page_number": 14,
  "content_type": "page_text",
  "character_count": 965
}
```

Content:
Complex RAG Parsing Sample - synthetic document
Page 14
13. Edge Cases for Parsers
The following cases often break real document ingestion pipelines. They are included here as guidance for testing parser
quality before moving to embeddings and vector storage.
Edge case
Example
Recommended handling
Repeated headers and
footers
Page number, confidentiality banner
Remove or store separately as metadata
Hyphenated line breaks
termi- nation assistance
Normalize during cleaning
Rotated tables
Landscape appendix in PDF
Use layout-aware parser or OCR
Merged cells
Pricing table with grouped plans
Preserve hierarchy in row text
Scanned signatures
Signature block as image
OCR if text is needed; store image reference
Boilerplate navigation
Website header and footer
Use boilerplate removal
Duplicate chunks
Same policy in FAQ and PDF
Deduplicate using source and hash
Bad parsing creates bad chunks. Bad chunks create bad retrieval. Bad retrieval creates bad answers.

---


# Document 15

Metadata:
```json
{
  "source": "C:\\Users\\Admin\\Agentic AI Projects\\AI\\RAG\\Langchain-use\\data\\Client_Contracts_Policies_and_Incident_Records.pdf",
  "page_number": 15,
  "content_type": "page_text",
  "character_count": 1145
}
```

Content:
Complex RAG Parsing Sample - synthetic document
Page 15
15. Final Ingestion Checklist
Use this checklist before sending parsed content into chunking and embeddings. It helps identify whether the data is ready for
production RAG.
Checklist item
Status to verify
Why it matters
Text extraction
Paragraphs are readable and ordered
Prevents noisy chunks
Table extraction
Rows, columns, headers, and footnotes
preserved
Protects factual answers
Image handling
Captions indexed and OCR done if required
Avoids missing visual information
Metadata
source, page, client_id, document_id
captured
Enables citations and access control
Chunking
Chunks preserve meaning and section
boundaries
Improves retrieval relevance
Access control
Retrieval filters use authenticated client_id
Prevents data leakage
Evaluation
Golden questions tested with citations
Measures real answer quality
Summary: RAG is about knowledge access. Fine-tuning is about behavior adaptation. For document intelligence, parsing
quality is the foundation. If extraction is weak, no embedding model or LLM can fully fix the missing context.
End of synthetic 15-page parsing test document.

---


# Document 16

Metadata:
```json
{
  "source": "C:\\Users\\Admin\\Agentic AI Projects\\AI\\RAG\\Langchain-use\\data\\Client_Contracts_Policies_and_Incident_Records.pdf",
  "page_number": 16,
  "content_type": "page_text",
  "character_count": 569
}
```

Content:
Complex RAG Parsing Sample - appended complex tables
Appendix page 1
Appendix A: Complex Clause Responsibility Matrix
Grouped clauses with owner/backup split inside the same responsibility cell. This page is useful for testing row
grouping, merged-looking labels, split responsibility cells, and long evidence text.
Parsing challenge: preserve row boundaries, nested headers, split cells, grouped labels, numeric values, and footnotes/context around
the table.
Table 1: Added as complex parsing appendix for table extraction, OCR fallback, and layout-aware RAG testing.

---


# Document 17

Metadata:
```json
{
  "source": "C:\\Users\\Admin\\Agentic AI Projects\\AI\\RAG\\Langchain-use\\data\\Client_Contracts_Policies_and_Incident_Records.pdf",
  "page_number": 17,
  "content_type": "page_text",
  "character_count": 511
}
```

Content:
Complex RAG Parsing Sample - appended complex tables
Appendix page 2
Appendix B: Regional Pricing and Usage Add-on Matrix
Pricing table with multi-level headers, regional columns, add-on columns, billing rules, exception rows, and
mixed numeric/text values.
Parsing challenge: preserve row boundaries, nested headers, split cells, grouped labels, numeric values, and footnotes/context around
the table.
Table 2: Added as complex parsing appendix for table extraction, OCR fallback, and layout-aware RAG testing.

---


# Document 18

Metadata:
```json
{
  "source": "C:\\Users\\Admin\\Agentic AI Projects\\AI\\RAG\\Langchain-use\\data\\Client_Contracts_Policies_and_Incident_Records.pdf",
  "page_number": 18,
  "content_type": "page_text",
  "character_count": 527
}
```

Content:
Complex RAG Parsing Sample - appended complex tables
Appendix page 3
Appendix C: Invoice Line Items with Tax Split
Invoice-style line item table with item groups, quantity, rate, CGST/SGST split, totals, and summary row. Useful
for invoice parsing and tax extraction tests.
Parsing challenge: preserve row boundaries, nested headers, split cells, grouped labels, numeric values, and footnotes/context around
the table.
Table 3: Added as complex parsing appendix for table extraction, OCR fallback, and layout-aware RAG testing.

---


# Document 19

Metadata:
```json
{
  "source": "C:\\Users\\Admin\\Agentic AI Projects\\AI\\RAG\\Langchain-use\\data\\Client_Contracts_Policies_and_Incident_Records.pdf",
  "page_number": 19,
  "content_type": "page_text",
  "character_count": 553
}
```

Content:
Complex RAG Parsing Sample - appended visuals and scanned documents
Appendix page 1
Appendix D: Multimodal Document Processing Flow
Diagram-style image showing how PDFs, DOCX files, scanned invoices, Excel/CSV metadata, parser/OCR,
extracted text/tables/metadata, and RAG-ready chunks connect.
Parsing challenge: image text, arrows, labels, and captions may not appear in normal PDF text extraction. OCR or multimodal
parsing may be required.
Added at the end for complex image parsing, OCR fallback, layout-aware extraction, and multimodal RAG testing.

---


# Document 20

Metadata:
```json
{
  "source": "C:\\Users\\Admin\\Agentic AI Projects\\AI\\RAG\\Langchain-use\\data\\Client_Contracts_Policies_and_Incident_Records.pdf",
  "page_number": 20,
  "content_type": "page_text",
  "character_count": 504
}
```

Content:
Complex RAG Parsing Sample - appended visuals and scanned documents
Appendix page 2
Appendix E: Contract Risk Dashboard Image
Dashboard-style image containing a bar chart, legend, and small matrix. Useful for testing chart extraction,
numeric value capture, and caption-aware indexing.
Parsing challenge: extract chart title, bar values, legend labels, and table values from an embedded image.
Added at the end for complex image parsing, OCR fallback, layout-aware extraction, and multimodal RAG testing.

---


# Document 21

Metadata:
```json
{
  "source": "C:\\Users\\Admin\\Agentic AI Projects\\AI\\RAG\\Langchain-use\\data\\Client_Contracts_Policies_and_Incident_Records.pdf",
  "page_number": 21,
  "content_type": "page_text",
  "character_count": 513
}
```

Content:
Complex RAG Parsing Sample - appended visuals and scanned documents
Appendix page 3
Appendix F: Data Lineage and Access Boundary
Image
Lineage-map style image with nodes, arrows, access boundaries, and metadata badges. Useful for diagram
OCR and relationship extraction.
Parsing challenge: diagram text must be OCRed and mapped to relationships such as user auth, namespace, retrieval, and
LLM gateway.
Added at the end for complex image parsing, OCR fallback, layout-aware extraction, and multimodal RAG testing.

---


# Document 22

Metadata:
```json
{
  "source": "C:\\Users\\Admin\\Agentic AI Projects\\AI\\RAG\\Langchain-use\\data\\Client_Contracts_Policies_and_Incident_Records.pdf",
  "page_number": 22,
  "content_type": "page_text",
  "character_count": 605
}
```

Content:
Complex RAG Parsing Sample - appended visuals and scanned documents
Appendix page 4
Appendix G: Additional Scanned Invoice for OCR
Testing
Synthetic scanned tax invoice with vendor details, customer details, invoice number, GSTIN, line items, tax split,
total amount, payment terms, footer notes, approval stamp, and handwritten-style receipt text.
Parsing challenge: this page is intentionally embedded as an image-like scan. A normal text parser may miss invoice values
unless OCR is enabled.
Added at the end for complex image parsing, OCR fallback, layout-aware extraction, and multimodal RAG testing.

---


# Document 23

Metadata:
```json
{
  "source": "C:\\Users\\Admin\\Agentic AI Projects\\AI\\RAG\\Langchain-use\\data\\Client_Contracts_Policies_and_Incident_Records.pdf",
  "page_number": 23,
  "content_type": "page_text",
  "character_count": 577
}
```

Content:
Complex RAG Parsing Sample - appended visuals and scanned documents
Appendix page 5
Appendix H: Additional Scanned Utility Bill for OCR
Testing
Synthetic scanned utility bill with meter-style charges, usage rows, tax values, total payable amount, payment
terms, stamp, handwritten-style note, and noisy/rotated scan effects.
Parsing challenge: extract bill number, issuer, line items, usage quantity, tax split, total payable, and payment notes from a
scanned image.
Added at the end for complex image parsing, OCR fallback, layout-aware extraction, and multimodal RAG testing.

---


# Document 24

Metadata:
```json
{
  "source": "C:\\Users\\Admin\\Agentic AI Projects\\AI\\RAG\\Langchain-use\\data\\Client_Contracts_Policies_and_Incident_Records.pdf",
  "page_number": 24,
  "content_type": "page_text",
  "character_count": 1241
}
```

Content:
Complex RAG Parsing Sample - appended instructor image
Appendix page 6
Appendix I: Profile Image for Multimodal Parsing
This page adds a portrait-style image to test how a parser or multimodal RAG system handles photographic
content, captions, image metadata, and surrounding text. Text-only loaders may extract the caption but cannot
understand the visual content unless OCR, vision, or multimodal parsing is used.
Caption: Portrait-style instructor image with a bright background. Useful for testing image extraction, captioning,
person detection, layout preservation, and multimodal document understanding.
Element
Parsing Challenge
Expected Handling
Portrait image
Pixels are not selectable PDF text.
Extract image object or create visual summary with a
multimodal model.
Caption text
Caption should stay attached to image
context.
Preserve caption near the image in reading order.
Image metadata
File name, page, and bounding box may be
needed.
Store metadata for citation and retrieval.
RAG usage
Text-only chunks may miss visual details.
Use OCR or vision captioning before chunking if
visual content matters.
Added at the end for complex image parsing, multimodal RAG testing, caption grounding, and visual-content extraction checks.

---


# Document 25

Metadata:
```json
{
  "source": "C:\\Users\\Admin\\Agentic AI Projects\\AI\\RAG\\Langchain-use\\data\\Client_Contracts_Policies_and_Incident_Records.pdf",
  "page_number": 1,
  "content_type": "page_image",
  "image_path": "C:\\Users\\Admin\\Agentic AI Projects\\AI\\RAG\\Langchain-use\\data\\parsed_pdf_output\\page_images\\page_001.png",
  "image_type": "full_page_render",
  "resolution_scale": 2.0
}
```

Content:

PAGE 1 - FULL PAGE IMAGE

Image Path: C:\Users\Admin\Agentic AI Projects\AI\RAG\Langchain-use\data\parsed_pdf_output\page_images\page_001.png

🖼️ Vision LLM Integration:
This page image can be sent directly to multimodal LLMs:
- Claude Vision API
- GPT-4V
- Gemini Vision
- LLaVA

The image shows the complete page layout including:
- All text content
- Visual formatting
- Images and diagrams
- Table layouts


---


# Document 26

Metadata:
```json
{
  "source": "C:\\Users\\Admin\\Agentic AI Projects\\AI\\RAG\\Langchain-use\\data\\Client_Contracts_Policies_and_Incident_Records.pdf",
  "page_number": 2,
  "content_type": "page_image",
  "image_path": "C:\\Users\\Admin\\Agentic AI Projects\\AI\\RAG\\Langchain-use\\data\\parsed_pdf_output\\page_images\\page_002.png",
  "image_type": "full_page_render",
  "resolution_scale": 2.0
}
```

Content:

PAGE 2 - FULL PAGE IMAGE

Image Path: C:\Users\Admin\Agentic AI Projects\AI\RAG\Langchain-use\data\parsed_pdf_output\page_images\page_002.png

🖼️ Vision LLM Integration:
This page image can be sent directly to multimodal LLMs:
- Claude Vision API
- GPT-4V
- Gemini Vision
- LLaVA

The image shows the complete page layout including:
- All text content
- Visual formatting
- Images and diagrams
- Table layouts


---


# Document 27

Metadata:
```json
{
  "source": "C:\\Users\\Admin\\Agentic AI Projects\\AI\\RAG\\Langchain-use\\data\\Client_Contracts_Policies_and_Incident_Records.pdf",
  "page_number": 3,
  "content_type": "page_image",
  "image_path": "C:\\Users\\Admin\\Agentic AI Projects\\AI\\RAG\\Langchain-use\\data\\parsed_pdf_output\\page_images\\page_003.png",
  "image_type": "full_page_render",
  "resolution_scale": 2.0
}
```

Content:

PAGE 3 - FULL PAGE IMAGE

Image Path: C:\Users\Admin\Agentic AI Projects\AI\RAG\Langchain-use\data\parsed_pdf_output\page_images\page_003.png

🖼️ Vision LLM Integration:
This page image can be sent directly to multimodal LLMs:
- Claude Vision API
- GPT-4V
- Gemini Vision
- LLaVA

The image shows the complete page layout including:
- All text content
- Visual formatting
- Images and diagrams
- Table layouts


---


# Document 28

Metadata:
```json
{
  "source": "C:\\Users\\Admin\\Agentic AI Projects\\AI\\RAG\\Langchain-use\\data\\Client_Contracts_Policies_and_Incident_Records.pdf",
  "page_number": 4,
  "content_type": "page_image",
  "image_path": "C:\\Users\\Admin\\Agentic AI Projects\\AI\\RAG\\Langchain-use\\data\\parsed_pdf_output\\page_images\\page_004.png",
  "image_type": "full_page_render",
  "resolution_scale": 2.0
}
```

Content:

PAGE 4 - FULL PAGE IMAGE

Image Path: C:\Users\Admin\Agentic AI Projects\AI\RAG\Langchain-use\data\parsed_pdf_output\page_images\page_004.png

🖼️ Vision LLM Integration:
This page image can be sent directly to multimodal LLMs:
- Claude Vision API
- GPT-4V
- Gemini Vision
- LLaVA

The image shows the complete page layout including:
- All text content
- Visual formatting
- Images and diagrams
- Table layouts


---


# Document 29

Metadata:
```json
{
  "source": "C:\\Users\\Admin\\Agentic AI Projects\\AI\\RAG\\Langchain-use\\data\\Client_Contracts_Policies_and_Incident_Records.pdf",
  "page_number": 5,
  "content_type": "page_image",
  "image_path": "C:\\Users\\Admin\\Agentic AI Projects\\AI\\RAG\\Langchain-use\\data\\parsed_pdf_output\\page_images\\page_005.png",
  "image_type": "full_page_render",
  "resolution_scale": 2.0
}
```

Content:

PAGE 5 - FULL PAGE IMAGE

Image Path: C:\Users\Admin\Agentic AI Projects\AI\RAG\Langchain-use\data\parsed_pdf_output\page_images\page_005.png

🖼️ Vision LLM Integration:
This page image can be sent directly to multimodal LLMs:
- Claude Vision API
- GPT-4V
- Gemini Vision
- LLaVA

The image shows the complete page layout including:
- All text content
- Visual formatting
- Images and diagrams
- Table layouts


---


# Document 30

Metadata:
```json
{
  "source": "C:\\Users\\Admin\\Agentic AI Projects\\AI\\RAG\\Langchain-use\\data\\Client_Contracts_Policies_and_Incident_Records.pdf",
  "page_number": 6,
  "content_type": "page_image",
  "image_path": "C:\\Users\\Admin\\Agentic AI Projects\\AI\\RAG\\Langchain-use\\data\\parsed_pdf_output\\page_images\\page_006.png",
  "image_type": "full_page_render",
  "resolution_scale": 2.0
}
```

Content:

PAGE 6 - FULL PAGE IMAGE

Image Path: C:\Users\Admin\Agentic AI Projects\AI\RAG\Langchain-use\data\parsed_pdf_output\page_images\page_006.png

🖼️ Vision LLM Integration:
This page image can be sent directly to multimodal LLMs:
- Claude Vision API
- GPT-4V
- Gemini Vision
- LLaVA

The image shows the complete page layout including:
- All text content
- Visual formatting
- Images and diagrams
- Table layouts


---


# Document 31

Metadata:
```json
{
  "source": "C:\\Users\\Admin\\Agentic AI Projects\\AI\\RAG\\Langchain-use\\data\\Client_Contracts_Policies_and_Incident_Records.pdf",
  "page_number": 7,
  "content_type": "page_image",
  "image_path": "C:\\Users\\Admin\\Agentic AI Projects\\AI\\RAG\\Langchain-use\\data\\parsed_pdf_output\\page_images\\page_007.png",
  "image_type": "full_page_render",
  "resolution_scale": 2.0
}
```

Content:

PAGE 7 - FULL PAGE IMAGE

Image Path: C:\Users\Admin\Agentic AI Projects\AI\RAG\Langchain-use\data\parsed_pdf_output\page_images\page_007.png

🖼️ Vision LLM Integration:
This page image can be sent directly to multimodal LLMs:
- Claude Vision API
- GPT-4V
- Gemini Vision
- LLaVA

The image shows the complete page layout including:
- All text content
- Visual formatting
- Images and diagrams
- Table layouts


---


# Document 32

Metadata:
```json
{
  "source": "C:\\Users\\Admin\\Agentic AI Projects\\AI\\RAG\\Langchain-use\\data\\Client_Contracts_Policies_and_Incident_Records.pdf",
  "page_number": 8,
  "content_type": "page_image",
  "image_path": "C:\\Users\\Admin\\Agentic AI Projects\\AI\\RAG\\Langchain-use\\data\\parsed_pdf_output\\page_images\\page_008.png",
  "image_type": "full_page_render",
  "resolution_scale": 2.0
}
```

Content:

PAGE 8 - FULL PAGE IMAGE

Image Path: C:\Users\Admin\Agentic AI Projects\AI\RAG\Langchain-use\data\parsed_pdf_output\page_images\page_008.png

🖼️ Vision LLM Integration:
This page image can be sent directly to multimodal LLMs:
- Claude Vision API
- GPT-4V
- Gemini Vision
- LLaVA

The image shows the complete page layout including:
- All text content
- Visual formatting
- Images and diagrams
- Table layouts


---


# Document 33

Metadata:
```json
{
  "source": "C:\\Users\\Admin\\Agentic AI Projects\\AI\\RAG\\Langchain-use\\data\\Client_Contracts_Policies_and_Incident_Records.pdf",
  "page_number": 9,
  "content_type": "page_image",
  "image_path": "C:\\Users\\Admin\\Agentic AI Projects\\AI\\RAG\\Langchain-use\\data\\parsed_pdf_output\\page_images\\page_009.png",
  "image_type": "full_page_render",
  "resolution_scale": 2.0
}
```

Content:

PAGE 9 - FULL PAGE IMAGE

Image Path: C:\Users\Admin\Agentic AI Projects\AI\RAG\Langchain-use\data\parsed_pdf_output\page_images\page_009.png

🖼️ Vision LLM Integration:
This page image can be sent directly to multimodal LLMs:
- Claude Vision API
- GPT-4V
- Gemini Vision
- LLaVA

The image shows the complete page layout including:
- All text content
- Visual formatting
- Images and diagrams
- Table layouts


---


# Document 34

Metadata:
```json
{
  "source": "C:\\Users\\Admin\\Agentic AI Projects\\AI\\RAG\\Langchain-use\\data\\Client_Contracts_Policies_and_Incident_Records.pdf",
  "page_number": 10,
  "content_type": "page_image",
  "image_path": "C:\\Users\\Admin\\Agentic AI Projects\\AI\\RAG\\Langchain-use\\data\\parsed_pdf_output\\page_images\\page_010.png",
  "image_type": "full_page_render",
  "resolution_scale": 2.0
}
```

Content:

PAGE 10 - FULL PAGE IMAGE

Image Path: C:\Users\Admin\Agentic AI Projects\AI\RAG\Langchain-use\data\parsed_pdf_output\page_images\page_010.png

🖼️ Vision LLM Integration:
This page image can be sent directly to multimodal LLMs:
- Claude Vision API
- GPT-4V
- Gemini Vision
- LLaVA

The image shows the complete page layout including:
- All text content
- Visual formatting
- Images and diagrams
- Table layouts


---


# Document 35

Metadata:
```json
{
  "source": "C:\\Users\\Admin\\Agentic AI Projects\\AI\\RAG\\Langchain-use\\data\\Client_Contracts_Policies_and_Incident_Records.pdf",
  "page_number": 11,
  "content_type": "page_image",
  "image_path": "C:\\Users\\Admin\\Agentic AI Projects\\AI\\RAG\\Langchain-use\\data\\parsed_pdf_output\\page_images\\page_011.png",
  "image_type": "full_page_render",
  "resolution_scale": 2.0
}
```

Content:

PAGE 11 - FULL PAGE IMAGE

Image Path: C:\Users\Admin\Agentic AI Projects\AI\RAG\Langchain-use\data\parsed_pdf_output\page_images\page_011.png

🖼️ Vision LLM Integration:
This page image can be sent directly to multimodal LLMs:
- Claude Vision API
- GPT-4V
- Gemini Vision
- LLaVA

The image shows the complete page layout including:
- All text content
- Visual formatting
- Images and diagrams
- Table layouts


---


# Document 36

Metadata:
```json
{
  "source": "C:\\Users\\Admin\\Agentic AI Projects\\AI\\RAG\\Langchain-use\\data\\Client_Contracts_Policies_and_Incident_Records.pdf",
  "page_number": 12,
  "content_type": "page_image",
  "image_path": "C:\\Users\\Admin\\Agentic AI Projects\\AI\\RAG\\Langchain-use\\data\\parsed_pdf_output\\page_images\\page_012.png",
  "image_type": "full_page_render",
  "resolution_scale": 2.0
}
```

Content:

PAGE 12 - FULL PAGE IMAGE

Image Path: C:\Users\Admin\Agentic AI Projects\AI\RAG\Langchain-use\data\parsed_pdf_output\page_images\page_012.png

🖼️ Vision LLM Integration:
This page image can be sent directly to multimodal LLMs:
- Claude Vision API
- GPT-4V
- Gemini Vision
- LLaVA

The image shows the complete page layout including:
- All text content
- Visual formatting
- Images and diagrams
- Table layouts


---


# Document 37

Metadata:
```json
{
  "source": "C:\\Users\\Admin\\Agentic AI Projects\\AI\\RAG\\Langchain-use\\data\\Client_Contracts_Policies_and_Incident_Records.pdf",
  "page_number": 13,
  "content_type": "page_image",
  "image_path": "C:\\Users\\Admin\\Agentic AI Projects\\AI\\RAG\\Langchain-use\\data\\parsed_pdf_output\\page_images\\page_013.png",
  "image_type": "full_page_render",
  "resolution_scale": 2.0
}
```

Content:

PAGE 13 - FULL PAGE IMAGE

Image Path: C:\Users\Admin\Agentic AI Projects\AI\RAG\Langchain-use\data\parsed_pdf_output\page_images\page_013.png

🖼️ Vision LLM Integration:
This page image can be sent directly to multimodal LLMs:
- Claude Vision API
- GPT-4V
- Gemini Vision
- LLaVA

The image shows the complete page layout including:
- All text content
- Visual formatting
- Images and diagrams
- Table layouts


---


# Document 38

Metadata:
```json
{
  "source": "C:\\Users\\Admin\\Agentic AI Projects\\AI\\RAG\\Langchain-use\\data\\Client_Contracts_Policies_and_Incident_Records.pdf",
  "page_number": 14,
  "content_type": "page_image",
  "image_path": "C:\\Users\\Admin\\Agentic AI Projects\\AI\\RAG\\Langchain-use\\data\\parsed_pdf_output\\page_images\\page_014.png",
  "image_type": "full_page_render",
  "resolution_scale": 2.0
}
```

Content:

PAGE 14 - FULL PAGE IMAGE

Image Path: C:\Users\Admin\Agentic AI Projects\AI\RAG\Langchain-use\data\parsed_pdf_output\page_images\page_014.png

🖼️ Vision LLM Integration:
This page image can be sent directly to multimodal LLMs:
- Claude Vision API
- GPT-4V
- Gemini Vision
- LLaVA

The image shows the complete page layout including:
- All text content
- Visual formatting
- Images and diagrams
- Table layouts


---


# Document 39

Metadata:
```json
{
  "source": "C:\\Users\\Admin\\Agentic AI Projects\\AI\\RAG\\Langchain-use\\data\\Client_Contracts_Policies_and_Incident_Records.pdf",
  "page_number": 15,
  "content_type": "page_image",
  "image_path": "C:\\Users\\Admin\\Agentic AI Projects\\AI\\RAG\\Langchain-use\\data\\parsed_pdf_output\\page_images\\page_015.png",
  "image_type": "full_page_render",
  "resolution_scale": 2.0
}
```

Content:

PAGE 15 - FULL PAGE IMAGE

Image Path: C:\Users\Admin\Agentic AI Projects\AI\RAG\Langchain-use\data\parsed_pdf_output\page_images\page_015.png

🖼️ Vision LLM Integration:
This page image can be sent directly to multimodal LLMs:
- Claude Vision API
- GPT-4V
- Gemini Vision
- LLaVA

The image shows the complete page layout including:
- All text content
- Visual formatting
- Images and diagrams
- Table layouts


---


# Document 40

Metadata:
```json
{
  "source": "C:\\Users\\Admin\\Agentic AI Projects\\AI\\RAG\\Langchain-use\\data\\Client_Contracts_Policies_and_Incident_Records.pdf",
  "page_number": 16,
  "content_type": "page_image",
  "image_path": "C:\\Users\\Admin\\Agentic AI Projects\\AI\\RAG\\Langchain-use\\data\\parsed_pdf_output\\page_images\\page_016.png",
  "image_type": "full_page_render",
  "resolution_scale": 2.0
}
```

Content:

PAGE 16 - FULL PAGE IMAGE

Image Path: C:\Users\Admin\Agentic AI Projects\AI\RAG\Langchain-use\data\parsed_pdf_output\page_images\page_016.png

🖼️ Vision LLM Integration:
This page image can be sent directly to multimodal LLMs:
- Claude Vision API
- GPT-4V
- Gemini Vision
- LLaVA

The image shows the complete page layout including:
- All text content
- Visual formatting
- Images and diagrams
- Table layouts


---


# Document 41

Metadata:
```json
{
  "source": "C:\\Users\\Admin\\Agentic AI Projects\\AI\\RAG\\Langchain-use\\data\\Client_Contracts_Policies_and_Incident_Records.pdf",
  "page_number": 17,
  "content_type": "page_image",
  "image_path": "C:\\Users\\Admin\\Agentic AI Projects\\AI\\RAG\\Langchain-use\\data\\parsed_pdf_output\\page_images\\page_017.png",
  "image_type": "full_page_render",
  "resolution_scale": 2.0
}
```

Content:

PAGE 17 - FULL PAGE IMAGE

Image Path: C:\Users\Admin\Agentic AI Projects\AI\RAG\Langchain-use\data\parsed_pdf_output\page_images\page_017.png

🖼️ Vision LLM Integration:
This page image can be sent directly to multimodal LLMs:
- Claude Vision API
- GPT-4V
- Gemini Vision
- LLaVA

The image shows the complete page layout including:
- All text content
- Visual formatting
- Images and diagrams
- Table layouts


---


# Document 42

Metadata:
```json
{
  "source": "C:\\Users\\Admin\\Agentic AI Projects\\AI\\RAG\\Langchain-use\\data\\Client_Contracts_Policies_and_Incident_Records.pdf",
  "page_number": 18,
  "content_type": "page_image",
  "image_path": "C:\\Users\\Admin\\Agentic AI Projects\\AI\\RAG\\Langchain-use\\data\\parsed_pdf_output\\page_images\\page_018.png",
  "image_type": "full_page_render",
  "resolution_scale": 2.0
}
```

Content:

PAGE 18 - FULL PAGE IMAGE

Image Path: C:\Users\Admin\Agentic AI Projects\AI\RAG\Langchain-use\data\parsed_pdf_output\page_images\page_018.png

🖼️ Vision LLM Integration:
This page image can be sent directly to multimodal LLMs:
- Claude Vision API
- GPT-4V
- Gemini Vision
- LLaVA

The image shows the complete page layout including:
- All text content
- Visual formatting
- Images and diagrams
- Table layouts


---


# Document 43

Metadata:
```json
{
  "source": "C:\\Users\\Admin\\Agentic AI Projects\\AI\\RAG\\Langchain-use\\data\\Client_Contracts_Policies_and_Incident_Records.pdf",
  "page_number": 19,
  "content_type": "page_image",
  "image_path": "C:\\Users\\Admin\\Agentic AI Projects\\AI\\RAG\\Langchain-use\\data\\parsed_pdf_output\\page_images\\page_019.png",
  "image_type": "full_page_render",
  "resolution_scale": 2.0
}
```

Content:

PAGE 19 - FULL PAGE IMAGE

Image Path: C:\Users\Admin\Agentic AI Projects\AI\RAG\Langchain-use\data\parsed_pdf_output\page_images\page_019.png

🖼️ Vision LLM Integration:
This page image can be sent directly to multimodal LLMs:
- Claude Vision API
- GPT-4V
- Gemini Vision
- LLaVA

The image shows the complete page layout including:
- All text content
- Visual formatting
- Images and diagrams
- Table layouts


---


# Document 44

Metadata:
```json
{
  "source": "C:\\Users\\Admin\\Agentic AI Projects\\AI\\RAG\\Langchain-use\\data\\Client_Contracts_Policies_and_Incident_Records.pdf",
  "page_number": 20,
  "content_type": "page_image",
  "image_path": "C:\\Users\\Admin\\Agentic AI Projects\\AI\\RAG\\Langchain-use\\data\\parsed_pdf_output\\page_images\\page_020.png",
  "image_type": "full_page_render",
  "resolution_scale": 2.0
}
```

Content:

PAGE 20 - FULL PAGE IMAGE

Image Path: C:\Users\Admin\Agentic AI Projects\AI\RAG\Langchain-use\data\parsed_pdf_output\page_images\page_020.png

🖼️ Vision LLM Integration:
This page image can be sent directly to multimodal LLMs:
- Claude Vision API
- GPT-4V
- Gemini Vision
- LLaVA

The image shows the complete page layout including:
- All text content
- Visual formatting
- Images and diagrams
- Table layouts


---


# Document 45

Metadata:
```json
{
  "source": "C:\\Users\\Admin\\Agentic AI Projects\\AI\\RAG\\Langchain-use\\data\\Client_Contracts_Policies_and_Incident_Records.pdf",
  "page_number": 21,
  "content_type": "page_image",
  "image_path": "C:\\Users\\Admin\\Agentic AI Projects\\AI\\RAG\\Langchain-use\\data\\parsed_pdf_output\\page_images\\page_021.png",
  "image_type": "full_page_render",
  "resolution_scale": 2.0
}
```

Content:

PAGE 21 - FULL PAGE IMAGE

Image Path: C:\Users\Admin\Agentic AI Projects\AI\RAG\Langchain-use\data\parsed_pdf_output\page_images\page_021.png

🖼️ Vision LLM Integration:
This page image can be sent directly to multimodal LLMs:
- Claude Vision API
- GPT-4V
- Gemini Vision
- LLaVA

The image shows the complete page layout including:
- All text content
- Visual formatting
- Images and diagrams
- Table layouts


---


# Document 46

Metadata:
```json
{
  "source": "C:\\Users\\Admin\\Agentic AI Projects\\AI\\RAG\\Langchain-use\\data\\Client_Contracts_Policies_and_Incident_Records.pdf",
  "page_number": 22,
  "content_type": "page_image",
  "image_path": "C:\\Users\\Admin\\Agentic AI Projects\\AI\\RAG\\Langchain-use\\data\\parsed_pdf_output\\page_images\\page_022.png",
  "image_type": "full_page_render",
  "resolution_scale": 2.0
}
```

Content:

PAGE 22 - FULL PAGE IMAGE

Image Path: C:\Users\Admin\Agentic AI Projects\AI\RAG\Langchain-use\data\parsed_pdf_output\page_images\page_022.png

🖼️ Vision LLM Integration:
This page image can be sent directly to multimodal LLMs:
- Claude Vision API
- GPT-4V
- Gemini Vision
- LLaVA

The image shows the complete page layout including:
- All text content
- Visual formatting
- Images and diagrams
- Table layouts


---


# Document 47

Metadata:
```json
{
  "source": "C:\\Users\\Admin\\Agentic AI Projects\\AI\\RAG\\Langchain-use\\data\\Client_Contracts_Policies_and_Incident_Records.pdf",
  "page_number": 23,
  "content_type": "page_image",
  "image_path": "C:\\Users\\Admin\\Agentic AI Projects\\AI\\RAG\\Langchain-use\\data\\parsed_pdf_output\\page_images\\page_023.png",
  "image_type": "full_page_render",
  "resolution_scale": 2.0
}
```

Content:

PAGE 23 - FULL PAGE IMAGE

Image Path: C:\Users\Admin\Agentic AI Projects\AI\RAG\Langchain-use\data\parsed_pdf_output\page_images\page_023.png

🖼️ Vision LLM Integration:
This page image can be sent directly to multimodal LLMs:
- Claude Vision API
- GPT-4V
- Gemini Vision
- LLaVA

The image shows the complete page layout including:
- All text content
- Visual formatting
- Images and diagrams
- Table layouts


---


# Document 48

Metadata:
```json
{
  "source": "C:\\Users\\Admin\\Agentic AI Projects\\AI\\RAG\\Langchain-use\\data\\Client_Contracts_Policies_and_Incident_Records.pdf",
  "page_number": 24,
  "content_type": "page_image",
  "image_path": "C:\\Users\\Admin\\Agentic AI Projects\\AI\\RAG\\Langchain-use\\data\\parsed_pdf_output\\page_images\\page_024.png",
  "image_type": "full_page_render",
  "resolution_scale": 2.0
}
```

Content:

PAGE 24 - FULL PAGE IMAGE

Image Path: C:\Users\Admin\Agentic AI Projects\AI\RAG\Langchain-use\data\parsed_pdf_output\page_images\page_024.png

🖼️ Vision LLM Integration:
This page image can be sent directly to multimodal LLMs:
- Claude Vision API
- GPT-4V
- Gemini Vision
- LLaVA

The image shows the complete page layout including:
- All text content
- Visual formatting
- Images and diagrams
- Table layouts


---


# Document 49

Metadata:
```json
{
  "source": "C:\\Users\\Admin\\Agentic AI Projects\\AI\\RAG\\Langchain-use\\data\\Client_Contracts_Policies_and_Incident_Records.pdf",
  "page_number": 2,
  "content_type": "embedded_image",
  "image_path": "C:\\Users\\Admin\\Agentic AI Projects\\AI\\RAG\\Langchain-use\\data\\parsed_pdf_output\\extracted_images\\page_002_image_1.png",
  "image_index": 1,
  "image_ext": "png",
  "image_size_bytes": 20287
}
```

Content:

EMBEDDED IMAGE - Page 2, Image 1

Image Path: C:\Users\Admin\Agentic AI Projects\AI\RAG\Langchain-use\data\parsed_pdf_output\extracted_images\page_002_image_1.png

🖼️ Vision LLM Integration:
This embedded image can be sent directly to multimodal LLMs:
- Claude Vision API
- GPT-4V
- Gemini Vision
- LLaVA

Ask the vision LLM to describe, analyze, or extract information
from this image for better RAG context.


---


# Document 50

Metadata:
```json
{
  "source": "C:\\Users\\Admin\\Agentic AI Projects\\AI\\RAG\\Langchain-use\\data\\Client_Contracts_Policies_and_Incident_Records.pdf",
  "page_number": 7,
  "content_type": "embedded_image",
  "image_path": "C:\\Users\\Admin\\Agentic AI Projects\\AI\\RAG\\Langchain-use\\data\\parsed_pdf_output\\extracted_images\\page_007_image_1.png",
  "image_index": 1,
  "image_ext": "png",
  "image_size_bytes": 40915
}
```

Content:

EMBEDDED IMAGE - Page 7, Image 1

Image Path: C:\Users\Admin\Agentic AI Projects\AI\RAG\Langchain-use\data\parsed_pdf_output\extracted_images\page_007_image_1.png

🖼️ Vision LLM Integration:
This embedded image can be sent directly to multimodal LLMs:
- Claude Vision API
- GPT-4V
- Gemini Vision
- LLaVA

Ask the vision LLM to describe, analyze, or extract information
from this image for better RAG context.


---


# Document 51

Metadata:
```json
{
  "source": "C:\\Users\\Admin\\Agentic AI Projects\\AI\\RAG\\Langchain-use\\data\\Client_Contracts_Policies_and_Incident_Records.pdf",
  "page_number": 9,
  "content_type": "embedded_image",
  "image_path": "C:\\Users\\Admin\\Agentic AI Projects\\AI\\RAG\\Langchain-use\\data\\parsed_pdf_output\\extracted_images\\page_009_image_1.png",
  "image_index": 1,
  "image_ext": "png",
  "image_size_bytes": 34442
}
```

Content:

EMBEDDED IMAGE - Page 9, Image 1

Image Path: C:\Users\Admin\Agentic AI Projects\AI\RAG\Langchain-use\data\parsed_pdf_output\extracted_images\page_009_image_1.png

🖼️ Vision LLM Integration:
This embedded image can be sent directly to multimodal LLMs:
- Claude Vision API
- GPT-4V
- Gemini Vision
- LLaVA

Ask the vision LLM to describe, analyze, or extract information
from this image for better RAG context.


---


# Document 52

Metadata:
```json
{
  "source": "C:\\Users\\Admin\\Agentic AI Projects\\AI\\RAG\\Langchain-use\\data\\Client_Contracts_Policies_and_Incident_Records.pdf",
  "page_number": 12,
  "content_type": "embedded_image",
  "image_path": "C:\\Users\\Admin\\Agentic AI Projects\\AI\\RAG\\Langchain-use\\data\\parsed_pdf_output\\extracted_images\\page_012_image_1.png",
  "image_index": 1,
  "image_ext": "png",
  "image_size_bytes": 42329
}
```

Content:

EMBEDDED IMAGE - Page 12, Image 1

Image Path: C:\Users\Admin\Agentic AI Projects\AI\RAG\Langchain-use\data\parsed_pdf_output\extracted_images\page_012_image_1.png

🖼️ Vision LLM Integration:
This embedded image can be sent directly to multimodal LLMs:
- Claude Vision API
- GPT-4V
- Gemini Vision
- LLaVA

Ask the vision LLM to describe, analyze, or extract information
from this image for better RAG context.


---


# Document 53

Metadata:
```json
{
  "source": "C:\\Users\\Admin\\Agentic AI Projects\\AI\\RAG\\Langchain-use\\data\\Client_Contracts_Policies_and_Incident_Records.pdf",
  "page_number": 16,
  "content_type": "embedded_image",
  "image_path": "C:\\Users\\Admin\\Agentic AI Projects\\AI\\RAG\\Langchain-use\\data\\parsed_pdf_output\\extracted_images\\page_016_image_1.png",
  "image_index": 1,
  "image_ext": "png",
  "image_size_bytes": 50810
}
```

Content:

EMBEDDED IMAGE - Page 16, Image 1

Image Path: C:\Users\Admin\Agentic AI Projects\AI\RAG\Langchain-use\data\parsed_pdf_output\extracted_images\page_016_image_1.png

🖼️ Vision LLM Integration:
This embedded image can be sent directly to multimodal LLMs:
- Claude Vision API
- GPT-4V
- Gemini Vision
- LLaVA

Ask the vision LLM to describe, analyze, or extract information
from this image for better RAG context.


---


# Document 54

Metadata:
```json
{
  "source": "C:\\Users\\Admin\\Agentic AI Projects\\AI\\RAG\\Langchain-use\\data\\Client_Contracts_Policies_and_Incident_Records.pdf",
  "page_number": 17,
  "content_type": "embedded_image",
  "image_path": "C:\\Users\\Admin\\Agentic AI Projects\\AI\\RAG\\Langchain-use\\data\\parsed_pdf_output\\extracted_images\\page_017_image_1.png",
  "image_index": 1,
  "image_ext": "png",
  "image_size_bytes": 28524
}
```

Content:

EMBEDDED IMAGE - Page 17, Image 1

Image Path: C:\Users\Admin\Agentic AI Projects\AI\RAG\Langchain-use\data\parsed_pdf_output\extracted_images\page_017_image_1.png

🖼️ Vision LLM Integration:
This embedded image can be sent directly to multimodal LLMs:
- Claude Vision API
- GPT-4V
- Gemini Vision
- LLaVA

Ask the vision LLM to describe, analyze, or extract information
from this image for better RAG context.


---


# Document 55

Metadata:
```json
{
  "source": "C:\\Users\\Admin\\Agentic AI Projects\\AI\\RAG\\Langchain-use\\data\\Client_Contracts_Policies_and_Incident_Records.pdf",
  "page_number": 18,
  "content_type": "embedded_image",
  "image_path": "C:\\Users\\Admin\\Agentic AI Projects\\AI\\RAG\\Langchain-use\\data\\parsed_pdf_output\\extracted_images\\page_018_image_1.png",
  "image_index": 1,
  "image_ext": "png",
  "image_size_bytes": 18449
}
```

Content:

EMBEDDED IMAGE - Page 18, Image 1

Image Path: C:\Users\Admin\Agentic AI Projects\AI\RAG\Langchain-use\data\parsed_pdf_output\extracted_images\page_018_image_1.png

🖼️ Vision LLM Integration:
This embedded image can be sent directly to multimodal LLMs:
- Claude Vision API
- GPT-4V
- Gemini Vision
- LLaVA

Ask the vision LLM to describe, analyze, or extract information
from this image for better RAG context.


---


# Document 56

Metadata:
```json
{
  "source": "C:\\Users\\Admin\\Agentic AI Projects\\AI\\RAG\\Langchain-use\\data\\Client_Contracts_Policies_and_Incident_Records.pdf",
  "page_number": 19,
  "content_type": "embedded_image",
  "image_path": "C:\\Users\\Admin\\Agentic AI Projects\\AI\\RAG\\Langchain-use\\data\\parsed_pdf_output\\extracted_images\\page_019_image_1.png",
  "image_index": 1,
  "image_ext": "png",
  "image_size_bytes": 38663
}
```

Content:

EMBEDDED IMAGE - Page 19, Image 1

Image Path: C:\Users\Admin\Agentic AI Projects\AI\RAG\Langchain-use\data\parsed_pdf_output\extracted_images\page_019_image_1.png

🖼️ Vision LLM Integration:
This embedded image can be sent directly to multimodal LLMs:
- Claude Vision API
- GPT-4V
- Gemini Vision
- LLaVA

Ask the vision LLM to describe, analyze, or extract information
from this image for better RAG context.


---


# Document 57

Metadata:
```json
{
  "source": "C:\\Users\\Admin\\Agentic AI Projects\\AI\\RAG\\Langchain-use\\data\\Client_Contracts_Policies_and_Incident_Records.pdf",
  "page_number": 20,
  "content_type": "embedded_image",
  "image_path": "C:\\Users\\Admin\\Agentic AI Projects\\AI\\RAG\\Langchain-use\\data\\parsed_pdf_output\\extracted_images\\page_020_image_1.png",
  "image_index": 1,
  "image_ext": "png",
  "image_size_bytes": 47308
}
```

Content:

EMBEDDED IMAGE - Page 20, Image 1

Image Path: C:\Users\Admin\Agentic AI Projects\AI\RAG\Langchain-use\data\parsed_pdf_output\extracted_images\page_020_image_1.png

🖼️ Vision LLM Integration:
This embedded image can be sent directly to multimodal LLMs:
- Claude Vision API
- GPT-4V
- Gemini Vision
- LLaVA

Ask the vision LLM to describe, analyze, or extract information
from this image for better RAG context.


---


# Document 58

Metadata:
```json
{
  "source": "C:\\Users\\Admin\\Agentic AI Projects\\AI\\RAG\\Langchain-use\\data\\Client_Contracts_Policies_and_Incident_Records.pdf",
  "page_number": 21,
  "content_type": "embedded_image",
  "image_path": "C:\\Users\\Admin\\Agentic AI Projects\\AI\\RAG\\Langchain-use\\data\\parsed_pdf_output\\extracted_images\\page_021_image_1.png",
  "image_index": 1,
  "image_ext": "png",
  "image_size_bytes": 40012
}
```

Content:

EMBEDDED IMAGE - Page 21, Image 1

Image Path: C:\Users\Admin\Agentic AI Projects\AI\RAG\Langchain-use\data\parsed_pdf_output\extracted_images\page_021_image_1.png

🖼️ Vision LLM Integration:
This embedded image can be sent directly to multimodal LLMs:
- Claude Vision API
- GPT-4V
- Gemini Vision
- LLaVA

Ask the vision LLM to describe, analyze, or extract information
from this image for better RAG context.


---


# Document 59

Metadata:
```json
{
  "source": "C:\\Users\\Admin\\Agentic AI Projects\\AI\\RAG\\Langchain-use\\data\\Client_Contracts_Policies_and_Incident_Records.pdf",
  "page_number": 22,
  "content_type": "embedded_image",
  "image_path": "C:\\Users\\Admin\\Agentic AI Projects\\AI\\RAG\\Langchain-use\\data\\parsed_pdf_output\\extracted_images\\page_022_image_1.png",
  "image_index": 1,
  "image_ext": "png",
  "image_size_bytes": 157519
}
```

Content:

EMBEDDED IMAGE - Page 22, Image 1

Image Path: C:\Users\Admin\Agentic AI Projects\AI\RAG\Langchain-use\data\parsed_pdf_output\extracted_images\page_022_image_1.png

🖼️ Vision LLM Integration:
This embedded image can be sent directly to multimodal LLMs:
- Claude Vision API
- GPT-4V
- Gemini Vision
- LLaVA

Ask the vision LLM to describe, analyze, or extract information
from this image for better RAG context.


---


# Document 60

Metadata:
```json
{
  "source": "C:\\Users\\Admin\\Agentic AI Projects\\AI\\RAG\\Langchain-use\\data\\Client_Contracts_Policies_and_Incident_Records.pdf",
  "page_number": 23,
  "content_type": "embedded_image",
  "image_path": "C:\\Users\\Admin\\Agentic AI Projects\\AI\\RAG\\Langchain-use\\data\\parsed_pdf_output\\extracted_images\\page_023_image_1.png",
  "image_index": 1,
  "image_ext": "png",
  "image_size_bytes": 152573
}
```

Content:

EMBEDDED IMAGE - Page 23, Image 1

Image Path: C:\Users\Admin\Agentic AI Projects\AI\RAG\Langchain-use\data\parsed_pdf_output\extracted_images\page_023_image_1.png

🖼️ Vision LLM Integration:
This embedded image can be sent directly to multimodal LLMs:
- Claude Vision API
- GPT-4V
- Gemini Vision
- LLaVA

Ask the vision LLM to describe, analyze, or extract information
from this image for better RAG context.


---


# Document 61

Metadata:
```json
{
  "source": "C:\\Users\\Admin\\Agentic AI Projects\\AI\\RAG\\Langchain-use\\data\\Client_Contracts_Policies_and_Incident_Records.pdf",
  "page_number": 24,
  "content_type": "embedded_image",
  "image_path": "C:\\Users\\Admin\\Agentic AI Projects\\AI\\RAG\\Langchain-use\\data\\parsed_pdf_output\\extracted_images\\page_024_image_1.jpeg",
  "image_index": 1,
  "image_ext": "jpeg",
  "image_size_bytes": 548862
}
```

Content:

EMBEDDED IMAGE - Page 24, Image 1

Image Path: C:\Users\Admin\Agentic AI Projects\AI\RAG\Langchain-use\data\parsed_pdf_output\extracted_images\page_024_image_1.jpeg

🖼️ Vision LLM Integration:
This embedded image can be sent directly to multimodal LLMs:
- Claude Vision API
- GPT-4V
- Gemini Vision
- LLaVA

Ask the vision LLM to describe, analyze, or extract information
from this image for better RAG context.


---


# Document 62

Metadata:
```json
{
  "source": "C:\\Users\\Admin\\Agentic AI Projects\\AI\\RAG\\Langchain-use\\data\\Client_Contracts_Policies_and_Incident_Records.pdf",
  "page_number": 1,
  "content_type": "table",
  "table_index": 1
}
```

Content:

TABLE - Page 1, Table 1

| Section               | Parsing challenge                       | Why it matters for RAG                  |
|:----------------------|:----------------------------------------|:----------------------------------------|
| Contracts             | Dense legal text, clause numbers, cross | Need section-aware chunks and citations |
|                       | references                              |                                         |
| Tables                | Merged headers, numeric columns,        | Need row/column preservation            |
|                       | footnotes                               |                                         |
| Images                | Architecture diagram, heatmap, scanned  | Need OCR or multimodal extraction       |
|                       | form                                    |                                         |
| Multi-tenant metadata | client_id, document_id,                 | Need access-safe retrieval              |
|                       | contract_group_id                       |                                         |


---


# Document 63

Metadata:
```json
{
  "source": "C:\\Users\\Admin\\Agentic AI Projects\\AI\\RAG\\Langchain-use\\data\\Client_Contracts_Policies_and_Incident_Records.pdf",
  "page_number": 2,
  "content_type": "table",
  "table_index": 1
}
```

Content:

TABLE - Page 2, Table 1

| Client            | Main document family        | Risk   | Primary users        | Typical question                    |
|:------------------|:----------------------------|:-------|:---------------------|:------------------------------------|
| Arka Finance      | MSA, audit addendum, DPA    | High   | Legal and compliance | What audit rights exist in the DPA? |
| BlueLeaf Retail   | MSA, pricing, support SLA   | Medium | Procurement          | Which clause controls renewal       |
|                   |                             |        |                      | pricing?                            |
| CityRide Mobility | Ops reports, incident logs, | Medium | Operations           | Which depot had repeated battery    |
|                   | SOPs                        |        |                      | incidents?                          |


---


# Document 64

Metadata:
```json
{
  "source": "C:\\Users\\Admin\\Agentic AI Projects\\AI\\RAG\\Langchain-use\\data\\Client_Contracts_Policies_and_Incident_Records.pdf",
  "page_number": 3,
  "content_type": "table",
  "table_index": 1
}
```

Content:

TABLE - Page 3, Table 1

| Asset ID     | Client            | Format      | Pages/Rows   | Expected extraction          | Notes                         |
|:-------------|:------------------|:------------|:-------------|:-----------------------------|:------------------------------|
| ARK-MSA-001  | Arka Finance      | PDF         | 32 pages     | Clauses, tables, signatures  | Born-digital text with footer |
|              |                   |             |              |                              | references                    |
| ARK-DPA-002  | Arka Finance      | DOCX        | 18 pages     | Headings, lists, tables      | Track changes removed         |
|              |                   |             |              |                              | before ingestion              |
| BLR-PRICE-00 | BlueLeaf Retail   | XLSX        | 12 sheets    | Rate cards, discounts        | Merged cells and formulas     |
| 3            |                   |             |              |                              |                               |
| BLR-SLA-004  | BlueLeaf Retail   | PDF         | 9 pages      | SLA table, escalation matrix | Table crosses page boundary   |
| CRM-OPS-005  | CityRide Mobility | CSV         | 48,200 rows  | Incident records             | Needs column type             |
|              |                   |             |              |                              | normalization                 |
| CRM-FORM-00  | CityRide Mobility | Scanned PDF | 4 pages      | OCR fields, checkbox         | Low contrast and slight       |
| 6            |                   |             |              |                              | rotation                      |
| KB-RUN-007   | Shared            | Markdown    | 14 files     | Runbook sections             | Good for heading-based        |
|              |                   |             |              |                              | chunks                        |
| WEB-FAQ-008  | Shared            | HTML        | 23 pages     | FAQ content, links           | Needs boilerplate removal     |


---


# Document 65

Metadata:
```json
{
  "source": "C:\\Users\\Admin\\Agentic AI Projects\\AI\\RAG\\Langchain-use\\data\\Client_Contracts_Policies_and_Incident_Records.pdf",
  "page_number": 4,
  "content_type": "table",
  "table_index": 1
}
```

Content:

TABLE - Page 4, Table 1

|   Clause | Short name      | Owner            | Trigger                 | Required action                          | Citation hint   |
|---------:|:----------------|:-----------------|:------------------------|:-----------------------------------------|:----------------|
|      7.2 | Confidentiality | Receiving Party  | Receipt of confidential | Protect information with reasonable care | Page 4, clause  |
|          |                 |                  | material                | and equivalent internal controls         | 7.2             |
|      9.1 | Data residency  | Service Provider | SOW specifies region    | Process production records only in       | Page 4, clause  |
|          |                 |                  |                         | approved region                          | 9.1             |
|     11.4 | Termination     | Service Provider | Agreement               | Provide export window for 30 days        | Page 4, clause  |
|          | assistance      |                  | termination             |                                          | 11.4            |


---


# Document 66

Metadata:
```json
{
  "source": "C:\\Users\\Admin\\Agentic AI Projects\\AI\\RAG\\Langchain-use\\data\\Client_Contracts_Policies_and_Incident_Records.pdf",
  "page_number": 5,
  "content_type": "table",
  "table_index": 1
}
```

Content:

TABLE - Page 5, Table 1

| Policy Area       | Rule                                                 | Owner            | Review Cycle        |
|:------------------|:-----------------------------------------------------|:-----------------|:--------------------|
| Refunds           | Refund requests must be raised within 7 days of      | Customer Support | Quarterly           |
|                   | purchase.                                            |                  |                     |
| Data Export       | Client admins can request export in CSV or JSON      | Platform Ops     | Monthly             |
|                   | format.                                              |                  |                     |
| Access Review     | Privileged access must be reviewed every 30 days.    | Security         | Monthly             |
| Incident Response | Critical incidents require acknowledgement within 30 | SRE              | After each incident |
|                   | minutes.                                             |                  |                     |
| Vendor Review     | High-risk vendors require annual risk assessment.    | Procurement      | Annual              |


---


# Document 67

Metadata:
```json
{
  "source": "C:\\Users\\Admin\\Agentic AI Projects\\AI\\RAG\\Langchain-use\\data\\Client_Contracts_Policies_and_Incident_Records.pdf",
  "page_number": 6,
  "content_type": "table",
  "table_index": 1
}
```

Content:

TABLE - Page 6, Table 1

| Service Category   | Severity       | Response Target   | Resolution Target   | Service Credit         | Evidence Required              |
|:-------------------|:---------------|:------------------|:--------------------|:-----------------------|:-------------------------------|
| API Availability   | P1 - complete  | 15 minutes        | 4 hours             | 10 percent monthly     | Monitoring logs and incident   |
|                    | outage         |                   |                     | fee credit             | ticket                         |
| API Availability   | P2 - degraded  | 30 minutes        | 8 hours             | 5 percent monthly fee  | Latency dashboard and          |
|                    | performance    |                   |                     | credit                 | affected endpoint list         |
| Data Pipeline      | P1 - ingestion | 20 minutes        | 6 hours             | 8 percent pipeline fee | Queue depth, failed job IDs,   |
|                    | stopped        |                   |                     | credit                 | replay report                  |
| Data Pipeline      | P3 - delayed   | 4 hours           | Next business day   | No automatic credit    | Batch ID and SLA exception     |
|                    | batch          |                   |                     |                        | note                           |
| Support            | P2 - urgent    | 1 hour            | 1 business day      | 2 percent support fee  | Support ticket with timestamps |
|                    | support        |                   |                     | credit                 |                                |


---


# Document 68

Metadata:
```json
{
  "source": "C:\\Users\\Admin\\Agentic AI Projects\\AI\\RAG\\Langchain-use\\data\\Client_Contracts_Policies_and_Incident_Records.pdf",
  "page_number": 7,
  "content_type": "table",
  "table_index": 1
}
```

Content:

TABLE - Page 7, Table 1

| Image element   | Potential extraction method    | Expected output                      |
|:----------------|:-------------------------------|:-------------------------------------|
| Box labels      | OCR or vision model            | Raw Files, Parser, Chunks, Vector DB |
| Arrows          | Layout or vision understanding | Processing order                     |
| Caption         | Normal PDF text extraction     | Description of the diagram           |


---


# Document 69

Metadata:
```json
{
  "source": "C:\\Users\\Admin\\Agentic AI Projects\\AI\\RAG\\Langchain-use\\data\\Client_Contracts_Policies_and_Incident_Records.pdf",
  "page_number": 8,
  "content_type": "table",
  "table_index": 1
}
```

Content:

TABLE - Page 8, Table 1

| Runbook field   | Value                      | Parsing expectation                     |
|:----------------|:---------------------------|:----------------------------------------|
| Title           | Contract Ingestion Failure | Should become section title metadata    |
| Symptoms        | Five bullet items          | Should remain as list or separate lines |
| Recovery Steps  | Numbered sequence          | Order must be preserved                 |


---


# Document 70

Metadata:
```json
{
  "source": "C:\\Users\\Admin\\Agentic AI Projects\\AI\\RAG\\Langchain-use\\data\\Client_Contracts_Policies_and_Incident_Records.pdf",
  "page_number": 9,
  "content_type": "table",
  "table_index": 1
}
```

Content:

TABLE - Page 9, Table 1

| Field             | Expected OCR value      | Validation rule                      |
|:------------------|:------------------------|:-------------------------------------|
| Client Name       | BlueLeaf Retail Pvt Ltd | Must match known client list         |
| Contract ID       | BLR-MSA-2026-019        | Pattern: client-code + type + year + |
|                   |                         | sequence                             |
| Effective Date    | 01 Apr 2026             | Date parser should normalize to ISO  |
|                   |                         | format                               |
| Approval checkbox | Checked                 | Boolean extraction required          |


---


# Document 71

Metadata:
```json
{
  "source": "C:\\Users\\Admin\\Agentic AI Projects\\AI\\RAG\\Langchain-use\\data\\Client_Contracts_Policies_and_Incident_Records.pdf",
  "page_number": 10,
  "content_type": "table",
  "table_index": 1
}
```

Content:

TABLE - Page 10, Table 1

| document_id   | document_type     | contract_group_id   | effective_date   | relationship                       |
|:--------------|:------------------|:--------------------|:-----------------|:-----------------------------------|
| BLR-MSA-001   | Master Service    | BLR-ACME-2026       | 2026-04-01       | Base commercial agreement          |
|               | Agreement         |                     |                  |                                    |
| BLR-NDA-002   | NDA               | BLR-ACME-2026       | 2026-04-01       | Confidentiality terms              |
| BLR-SOW-003   | Statement of Work | BLR-ACME-2026       | 2026-04-15       | Project scope and deliverables     |
| BLR-PRICE-004 | Pricing Amendment | BLR-ACME-2026       | 2026-05-01       | Updated pricing and discount tiers |
| BLR-SLA-005   | Support SLA       | BLR-ACME-2026       | 2026-05-10       | Support response and credits       |


---


# Document 72

Metadata:
```json
{
  "source": "C:\\Users\\Admin\\Agentic AI Projects\\AI\\RAG\\Langchain-use\\data\\Client_Contracts_Policies_and_Incident_Records.pdf",
  "page_number": 11,
  "content_type": "table",
  "table_index": 1
}
```

Content:

TABLE - Page 11, Table 1

| Layer               | Control                              | Failure mode if missing                     |
|:--------------------|:-------------------------------------|:--------------------------------------------|
| Authentication      | Identify user and organization       | Unknown user may access application         |
| Authorization       | Map user to client_id and role       | User may retrieve another clients documents |
| Vector retrieval    | Filter by client_id or namespace     | Retriever may return unauthorized chunks    |
| Prompt construction | Send only allowed context            | LLM may see sensitive data                  |
| Audit logging       | Record query, source chunks, user_id | No traceability during incident review      |


---


# Document 73

Metadata:
```json
{
  "source": "C:\\Users\\Admin\\Agentic AI Projects\\AI\\RAG\\Langchain-use\\data\\Client_Contracts_Policies_and_Incident_Records.pdf",
  "page_number": 12,
  "content_type": "table",
  "table_index": 1
}
```

Content:

TABLE - Page 12, Table 1

| Observation                | Supporting value        | Scheduling implication                           |
|:---------------------------|:------------------------|:-------------------------------------------------|
| Prime Friday performs best | 93 retention score      | Place premium content in Friday late/prime slots |
| Early week late slots      | 10 to 21 score range    | Avoid launching new series in weak slots         |
| underperform               |                         |                                                  |
| Evening improves midweek   | 77 on Wednesday evening | Use midweek evening for discovery content        |


---


# Document 74

Metadata:
```json
{
  "source": "C:\\Users\\Admin\\Agentic AI Projects\\AI\\RAG\\Langchain-use\\data\\Client_Contracts_Policies_and_Incident_Records.pdf",
  "page_number": 13,
  "content_type": "table",
  "table_index": 1
}
```

Content:

TABLE - Page 13, Table 1

| Test ID   | Question                        | Expected source    | Expected answer element    | Failure signal      |
|:----------|:--------------------------------|:-------------------|:---------------------------|:--------------------|
| Q-001     | What is the refund window?      | Policy Rules table | 7 days                     | Answer says 30 days |
| Q-002     | Which clause covers data        | Clause 9.1         | Approved processing region | No clause citation  |
|           | residency?                      |                    |                            |                     |
| Q-003     | What is P1 API response target? | SLA table          | 15 minutes                 | Wrong severity row  |
| Q-004     | Which documents belong to       | Relationship table | Five related documents     | Only one document   |
|           | BLR-ACME-2026?                  |                    |                            | returned            |
| Q-005     | Who owns access review?         | Policy Rules table | Security                   | Owner missing       |


---


# Document 75

Metadata:
```json
{
  "source": "C:\\Users\\Admin\\Agentic AI Projects\\AI\\RAG\\Langchain-use\\data\\Client_Contracts_Policies_and_Incident_Records.pdf",
  "page_number": 14,
  "content_type": "table",
  "table_index": 1
}
```

Content:

TABLE - Page 14, Table 1

| Edge case              | Example                             | Recommended handling                         |
|:-----------------------|:------------------------------------|:---------------------------------------------|
| Repeated headers and   | Page number, confidentiality banner | Remove or store separately as metadata       |
| footers                |                                     |                                              |
| Hyphenated line breaks | termi- nation assistance            | Normalize during cleaning                    |
| Rotated tables         | Landscape appendix in PDF           | Use layout-aware parser or OCR               |
| Merged cells           | Pricing table with grouped plans    | Preserve hierarchy in row text               |
| Scanned signatures     | Signature block as image            | OCR if text is needed; store image reference |
| Boilerplate navigation | Website header and footer           | Use boilerplate removal                      |
| Duplicate chunks       | Same policy in FAQ and PDF          | Deduplicate using source and hash            |


---


# Document 76

Metadata:
```json
{
  "source": "C:\\Users\\Admin\\Agentic AI Projects\\AI\\RAG\\Langchain-use\\data\\Client_Contracts_Policies_and_Incident_Records.pdf",
  "page_number": 15,
  "content_type": "table",
  "table_index": 1
}
```

Content:

TABLE - Page 15, Table 1

| Checklist item   | Status to verify                              | Why it matters                       |
|:-----------------|:----------------------------------------------|:-------------------------------------|
| Text extraction  | Paragraphs are readable and ordered           | Prevents noisy chunks                |
| Table extraction | Rows, columns, headers, and footnotes         | Protects factual answers             |
|                  | preserved                                     |                                      |
| Image handling   | Captions indexed and OCR done if required     | Avoids missing visual information    |
| Metadata         | source, page, client_id, document_id          | Enables citations and access control |
|                  | captured                                      |                                      |
| Chunking         | Chunks preserve meaning and section           | Improves retrieval relevance         |
|                  | boundaries                                    |                                      |
| Access control   | Retrieval filters use authenticated client_id | Prevents data leakage                |
| Evaluation       | Golden questions tested with citations        | Measures real answer quality         |


---


# Document 77

Metadata:
```json
{
  "source": "C:\\Users\\Admin\\Agentic AI Projects\\AI\\RAG\\Langchain-use\\data\\Client_Contracts_Policies_and_Incident_Records.pdf",
  "page_number": 24,
  "content_type": "table",
  "table_index": 1
}
```

Content:

TABLE - Page 24, Table 1

| Element        | Parsing Challenge                         | Expected Handling                                    |
|:---------------|:------------------------------------------|:-----------------------------------------------------|
| Portrait image | Pixels are not selectable PDF text.       | Extract image object or create visual summary with a |
|                |                                           | multimodal model.                                    |
| Caption text   | Caption should stay attached to image     | Preserve caption near the image in reading order.    |
|                | context.                                  |                                                      |
| Image metadata | File name, page, and bounding box may be  | Store metadata for citation and retrieval.           |
|                | needed.                                   |                                                      |
| RAG usage      | Text-only chunks may miss visual details. | Use OCR or vision captioning before chunking if      |
|                |                                           | visual content matters.                              |


---
