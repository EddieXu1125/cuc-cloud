from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from datetime import datetime, timedelta



def generate_selfsign(hostname):

    passphrase = b"passphrase"
    #Generate our key
    key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048)

    #生成私钥
    key_pem = key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption(passphrase),
    )

    #自签发证书

    name = x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME,hostname),
    ])

    now = datetime.utcnow()

    #path_length=0证明是自签发证书
    basic_contraints = x509.BasicConstraints(ca=True, path_length=0)
    
    cert=x509.CertificateBuilder().subject_name(
        name).issuer_name(
            name
        ).public_key(
            key.public_key()
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            now
        ).not_valid_after(
            now+datetime.timedelta(days=10) #10天有效期
        ).add_extension(
            x509.SubjectAlternativeName([x509.DNSName(hostname)]),
            critical=False
        ).add_extension(
            basic_contraints,False
        ).sign(key,hashes.SHA256())
        
    #证书
    cert_pem = cert.public_bytes(encoding=serialization.Encoding.PEM) 

    return cert_pem,key_pem