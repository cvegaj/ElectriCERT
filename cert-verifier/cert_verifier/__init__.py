"""
Verify blockchain certificates (http://www.blockcerts.org/)
"""

import binascii
import sys
from enum import Enum

from cert_verifier.errors import *

unhexlify = binascii.unhexlify
hexlify = binascii.hexlify
if sys.version > '3':
    def unhexlify(h): return binascii.unhexlify(h.encode('utf8'))


    def hexlify(b): return binascii.hexlify(b).decode('utf8')

StepStatus = Enum('StepStatus', ['not_started', 'done', 'passed', 'failed'])


class TransactionData:
    """
    If the blockchain transaction was found, this will be populated with signing key, the op_return script,
    the transaction time, and a set of revoked addresses for the transaction (pre-v2 only).

    These are the key parts of the transaction lookup that we need in validation.
    """

    def __init__(self, signing_key, op_return, date_time_utc, revoked_addresses):
        """

        :param signing_key: key used to sign the transaction
        :param op_return: value in op_return field
        :param date_time_utc: datetime in UTC
        :param revoked_addresses: revoked addresses (pre-V2)
        """
        self.signing_key = signing_key
        self.op_return = op_return
        self.date_time_utc = date_time_utc
        self.revoked_addresses = revoked_addresses


class IssuerInfo(object):
    """
    This is the issuer-hosted information that can be used for authenticity checks.

    IssuerInfo
        keys: Key[]
            - owner
            - created
            - creator
            - expires
            - revoked
            - publicKey
        revocation_keys: Key[] (pre-v2)
        revoked_assertions: string[] (v2)
    """

    def __init__(self, issuer_keys, revocation_keys=None, revoked_assertions=None):
        self.issuer_keys = issuer_keys
        self.revocation_keys = revocation_keys
        self.revoked_assertions = revoked_assertions


class IssuerKey(object):
    def __init__(self, public_key, created=None, expires=None, revoked=None):
        self.public_key = public_key
        self.created = created
        self.expires = expires
        self.revoked = revoked
