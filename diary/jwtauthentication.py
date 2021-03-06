import hashlib
import hmac
import json
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import (
    load_pem_private_key, load_pem_public_key, load_ssh_public_key
)
from cryptography.hazmat.primitives.asymmetric.rsa import (
    RSAPrivateKey, RSAPublicKey
)
from cryptography.hazmat.primitives.asymmetric.ec import (
    EllipticCurvePrivateKey, EllipticCurvePublicKey
)
from cryptography.hazmat.primitives.asymmetric import ec, padding
from cryptography.hazmat.backends import default_backend
from cryptography.exceptions import InvalidSignature
from base64 import b64decode, b64encode
from django.contrib.auth.models import User
from rest_framework import authentication
from rest_framework import exceptions
from django.conf import settings


class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth = authentication.get_authorization_header(request).split()
        if len(auth) != 2 or auth[0] != b'JWT':
            return None
        try:
            payload = self.decode_jwt(auth[1])
            user = User.objects.get(username=payload['username'])
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user')
        return user, payload

    def decode_jwt(self, token):
        (header, body, signature) = token.split(b'.')
        header_decoded = json.loads(b64decode(header).decode())
        if header_decoded['typ'] != 'JWT':
            raise exceptions.AuthenticationFailed('Not a JWT token')
        alg = header_decoded['alg']
        {
            'none': self.verify_none,
            'HS256': self.verify_hs256,
            'RS256': self.verify_rs256,
        }.get(alg, self.verify_fail)(header + b'.' + body, signature, settings.JWT_PUBLIC_KEY)
        body_decoded = json.loads(b64decode(body).decode())

        return body_decoded

    @staticmethod
    def verify_none(to_check, signature, secret):
        return True

    @staticmethod
    def verify_hs256(to_check, signature, secret):
        verify = b64encode(hmac.new(secret, to_check, hashlib.sha256).digest())
        if verify == signature:
            return True
        raise exceptions.AuthenticationFailed('Signature verification failed')

    @staticmethod
    def verify_rs256(to_check, signature, secret):
        key = load_pem_public_key(secret, backend=default_backend())
        verifier = key.verifier(b64decode(signature), padding.PKCS1v15(), hashes.SHA256())
        verifier.update(to_check)
        try:
            verifier.verify()
            return True
        except InvalidSignature:
            pass
        raise exceptions.AuthenticationFailed('Signature verification failed')

    @staticmethod
    def verify_fail(to_check, signature):
        raise exceptions.AuthenticationFailed('Algorithm type not supported')

    @staticmethod
    def create_jwt(token):
        header = b64encode(json.dumps({'typ': 'JWT', 'alg': 'RS256'}).encode())
        body = b64encode(json.dumps(token).encode())
        tosign = header + b'.' + body
        sig = JWTAuthentication.sign_rs256(tosign)
        return tosign + b'.' + sig

    @staticmethod
    def sign_rs256(to_check):
        key = load_pem_private_key(settings.JWT_PRIVATE_KEY, backend=default_backend(), password=None)
        signer = key.signer(padding.PKCS1v15(), hashes.SHA256())
        signer.update(to_check)
        return b64encode(signer.finalize())
