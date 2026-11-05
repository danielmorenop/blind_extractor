# Blind SQL Injection Extractor (PoC)
A Python-based Proof of Concept (PoC) script designed to automate data extraction in authorized testing environments using Boolean-based Blind SQL Injection. The script parses raw HTTP request files (like those exported from Burp Suite), injects payloads into designated markers, and evaluates boolean responses to reconstruct database strings character by character.

## Features
- Raw HTTP Request Parser (RequestParser): Automatically parses HTTP methods, headers, URLs, and body content from a simple text file.
- Dynamic Parameter Injection: Replaces custom markers (default: *) in the URL, headers, or body with the generated SQLi payloads.
- Character-by-character Extraction: Uses SUBSTR() functions and boolean comparisons to retrieve database content.
- Real-Time Progress: Utilizes the pwntools library to display a visual, real-time progress bar during the brute-force process.

## Prerequisites & Installation
- Python 3.8 or higher.
- Required Python libraries: pwntools, requests.

## Usage
Run the script by providing the path to your raw HTTP request file using the -f flag.

```python3 blind_extractor.py -f request.txt```

## Customizing the Target Data
By default, the script is configured to extract the database name (`database()`). You can modify the target query directly in the blind_extractor.py code by changing the `search` variable:

```
# Uncomment or modify the query you want to extract:
# search = "select group_concat(table_name) from information_schema.tables where table_schema='lab_db'"
search = "database()"
# search = "user()"
```
