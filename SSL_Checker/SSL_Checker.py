from OpenSSL import SSL
from cryptography import x509
from cryptography.x509.oid import NameOID
import idna
from datetime import datetime
from socket import socket
from collections import namedtuple
import concurrent.futures

HostInfo = namedtuple(field_names='cert hostname peername', typename='HostInfo')

HOSTS = [
    'damjan.softver.org.mk'
    'expired.badssl.com',
    'wrong.host.badssl.com'
]

def get_certificate(hostname, port):
    try:
        hostname_idna = idna.encode(hostname)
    
        sock = socket()

        sock.connect((hostname, port))
        peername = sock.getpeername()
        ctx = SSL.Context(SSL.SSLv23_METHOD) # most compatible
        ctx.check_hostname = False
        ctx.verify_mode = SSL.VERIFY_NONE

        sock_ssl = SSL.Connection(ctx, sock)
        sock_ssl.set_connect_state()
        sock_ssl.set_tlsext_host_name(hostname_idna)
        sock_ssl.do_handshake()
        cert = sock_ssl.get_peer_certificate()
        crypto_cert = cert.to_cryptography()
        sock_ssl.close()
        sock.close()

        return HostInfo(cert=crypto_cert, peername=peername, hostname=hostname)
    except:
        print(f"[+] Cannot Perfrom  Operation On Host: {hostname}")

def get_alt_names(cert):
    try:
        ext = cert.extensions.get_extension_for_class(x509.SubjectAlternativeName)
        return ext.value.get_values_for_type(x509.DNSName)
    except x509.ExtensionNotFound:
        return None

def get_common_name(cert):
    try:
        names = cert.subject.get_attributes_for_oid(NameOID.COMMON_NAME)
        return names[0].value
    except x509.ExtensionNotFound:
        return None

def get_issuer(cert):
    try:
        names = cert.issuer.get_attributes_for_oid(NameOID.COMMON_NAME)
        return names[0].value
    except x509.ExtensionNotFound:
        return None

def print_basic_info(hostinfo):
    s = '''» {hostname} « … {peername}
    \tcommonName: {commonname}
    \tSAN: {SAN}
    \tissuer: {issuer}
    \tnotBefore: {notbefore}
    \tnotAfter:  {notafter}
    '''.format(
            hostname=hostinfo.hostname,
            peername=hostinfo.peername,
            commonname=get_common_name(hostinfo.cert),
            SAN=get_alt_names(hostinfo.cert),
            issuer=get_issuer(hostinfo.cert),
            notbefore=hostinfo.cert.not_valid_before,
            notafter=hostinfo.cert.not_valid_after
    )
    print(s)

with concurrent.futures.ThreadPoolExecutor(max_workers=8) as e:
    for hostinfo in e.map(lambda x: get_certificate(x, 443), HOSTS):
        try:
            after_date=hostinfo.cert.not_valid_after
            today_date=datetime.now()
            days_left=after_date-today_date
            if days_left.days<=0:
                print("[+] Your Certificate Has Expired")
                print_basic_info(hostinfo)
            elif days_left.days<=30:
                print("[+] Your Certificate Will Expire in {} days".format(days_left.days))
        except:
            pass
