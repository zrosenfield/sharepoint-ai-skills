# Prompt 1 — Set up the list

Use the assertion-list-creator skill to create the Assertion Citations SharePoint list at https://{tenant}.sharepoint.com/sites/{site}. Configure Record, Statements, and Citations columns, with Citations as multi-line text supporting unlimited length.


# Prompt 2 — Extract assertions

Use the assertion-extractor skill to read {file path or SharePoint URL to the brief} and extract all factual assertions that need citations. Write each one as a new record to the Assertion Citations list at https://{tenant}.sharepoint.com/sites/{site}. Use the record ID prefix ZAVA-2025.


# Prompt 3 — Find citations

Use the citation-finder skill to process all records in the Assertion Citations list at https://{tenant}.sharepoint.com/sites/{site} that have an empty Citations field. Search for supporting sources in {SharePoint folder URL or local corpus path} and write the citation results back to each record.