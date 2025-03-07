import base64
import hashlib
import requests
from OpenSSL import crypto
from datetime import datetime
from urllib.parse import urlparse

# Load the .p12 file and extract the private key and certificate
def load_p12(p12_path, password):
    with open(p12_path, 'rb') as f:
        p12 = crypto.load_pkcs12(f.read(), password.encode())
    private_key = p12.get_privatekey()
    cert = p12.get_certificate()
    return private_key, cert

# Create the signature string and sign it using RSA-SHA512
def create_signature(private_key, request_target, host, date, digest):
    # Prepare the string to sign
    signature_string = f"(request-target): {request_target}\n" \
                       f"host: {host}\n" \
                       f"date: {date}\n" \
                       f"digest: {digest}"
    
    # Sign the string
    signature_bytes = crypto.sign(private_key, signature_string, 'sha512')
    
    # Base64 encode the signature
    return base64.b64encode(signature_bytes).decode()

# Generate the digest for the request body
def generate_digest(body):
    hash_bytes = hashlib.sha512(body.encode('utf-8')).digest()
    return "SHA-512=" + base64.b64encode(hash_bytes).decode()

# Main function to send the request
def send_signed_request(url, method, p12_path, p12_password, body):
    # Parse the URL to get the host and request target
    parsed_url = urlparse(url)
    host = parsed_url.netloc
    request_target = f"{method.lower()} {parsed_url.path}"
    
    # Generate current date in the required format
    date = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
    
    # Load the private key and certificate from the .p12 file
    private_key, cert = load_p12(p12_path, p12_password)
    
    # Generate the digest for the request body
    digest = generate_digest(body)
    
    # Create the signature
    signature = create_signature(private_key, request_target, host, date, digest)
    
    # Prepare the authorization header with the signature
    cert_b64 = base64.b64encode(crypto.dump_certificate(crypto.FILETYPE_ASN1, cert)).decode()
    auth_header = f'Signature keyId="{cert_b64}", algorithm="rsa-sha512", headers="(request-target) host date digest", signature="{signature}"'
    
    # Send the request with the necessary headers
    headers = {
        "Authorization": auth_header,
        "Date": date,
        "Host": host,
        "Digest": digest,
        "Content-Type": "application/json"
    }
    
    response = requests.request(method, url, headers=headers, data=body)
    return response

# Example usage
p12_path = "X0011839_03552800P.p12.bac"
p12_password = "Itptest1"
url = "https://softwaretestnextversion.ros.ie/customs/webservice/v1/rest/transactionID"
body = '<ns2:TransactionIDRequest xmlns:ns2="http://www.ros.ie/schemas/customs/transactionidrequest/v1"><ns2:Transactions><ns2:NumberOfTxIds>1</ns2:NumberOfTxIds></ns2:Transactions></ns2:TransactionIDRequest>'

# response = send_signed_request(url, 'POST', p12_path, p12_password, body)
# print(response.status_code, response.text)

print(load_p12(p12_path, p12_password))