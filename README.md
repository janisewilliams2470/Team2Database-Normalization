This repo contains Database & Normalization.
Own the shared schema: reports, facilities, contingencies, scenarios, findings, mitigations, evidence. They should handle 
canonical names, raw values like 119.0%, <100, NotConv, and traceability. This is the foundation everyone else depends on.

The Shared Schema-
 database.py file defines all seven required relational database models using SQLAlchemy:

    reports: Stores publication metadata and source documents.

    facilities: Houses assets and manages their standardized identities.

    contingencies: Tracks outage events and categories (e.g., P6, N-1-1).

    scenarios: Captures study operating conditions and timelines (e.g., Summer Peak).

    findings: The core fact table linking everything together.

    mitigations: Manages corrective solutions and RAS.

    evidence: Tracks page numbers, table coordinates, and source links.
    
db_url="sqlite:///power_system_reliability.db" points to a local file, SQLite will automatically collect all the facilities, contingencies, scenarios, and findings from future extractions and store them safely inside that single power_system_reliability.db file.
    
    
Handling Canonical Names-
 The Facility model:

    canonical_name = Column(String(150), unique=True, nullable=False)

Ensures that messy textual variations across different reports (like 24085 LUGO or lugo 230) can all be mapped to a single    unified, unique entry in the database.



Handling Raw Values-
normalizer.py script uses a dual-value strategy:

    raw_value preserves the exact text from the document (e.g., 119.0%, <100, or NotConv) for absolute auditing accuracy.

    parsed_value converts percentages and bounds into clean floats (e.g., 119.0, or 99.9 for bounds) so your team can run mathematical queries and filters.

    status_flag categorizes the results (OVERLOAD, BELOW_LIMIT, NOT_CONVERGED).


Traceability-
Evidence table links directly to the Finding model, capturing:

    source_document

    page_number

    table_reference
  This ensures that anyone querying a finding can immediately trace it back to the exact page and table of the source report

  

This can be ran on example data.

Next steps: Needs to connected to Team 1 - PDF Ingestion & Extraction. 
