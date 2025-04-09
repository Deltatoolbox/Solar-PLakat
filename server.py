from http.server import HTTPServer, SimpleHTTPRequestHandler
import ssl
import os
from datetime import datetime, timedelta
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
import ipaddress

def generate_self_signed_cert():
    # Generate private key
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    
    # Generate public key
    public_key = private_key.public_key()
    
    # Generate self-signed certificate
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, u"DE"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"Bavaria"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, u"Munich"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"Solar Panel Demo"),
        x509.NameAttribute(NameOID.COMMON_NAME, u"localhost"),
    ])
    
    cert = x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        issuer
    ).public_key(
        public_key
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.utcnow()
    ).not_valid_after(
        datetime.utcnow() + timedelta(days=20)
    ).add_extension(
        x509.SubjectAlternativeName([x509.DNSName(u"localhost")]),
        critical=False,
    ).sign(private_key, hashes.SHA256())
    
    # Write private key
    with open("key.pem", "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ))
    
    # Write certificate
    with open("cert.pem", "wb") as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))

class SecureRequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('X-Frame-Options', 'DENY')
        self.send_header('X-XSS-Protection', '1; mode=block')
        self.send_header('Strict-Transport-Security', 'max-age=31536000; includeSubDomains')
        self.send_header('Content-Security-Policy', "default-src 'self'")
        return super().end_headers()

def run(server_class=HTTPServer, handler_class=SecureRequestHandler, port=443):
    # Generate certificate if it doesn't exist
    if not (os.path.exists("cert.pem") and os.path.exists("key.pem")):
        print("Generating self-signed certificate...")
        generate_self_signed_cert()
        print("Certificate generated!")
    
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    
    # SSL configuration
    httpd.socket = ssl.wrap_socket(
        httpd.socket,
        keyfile="key.pem",
        certfile="cert.pem",
        server_side=True,
        ssl_version=ssl.PROTOCOL_TLS
    )
    
    print(f"Starting secure server on port {port}")
    print("Certificate is valid for 20 days from now")
    httpd.serve_forever()

if __name__ == '__main__':
    run() 