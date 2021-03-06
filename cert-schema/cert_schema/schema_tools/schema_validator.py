#! /usr/bin/env python

import json
import logging
import os
import re
from copy import deepcopy

try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen

import jsonschema
from pyld import jsonld
from pyld.jsonld import JsonLdProcessor

from cert_core import BLOCKCERTS_V2_SCHEMA

FALLBACK_VOCAB = 'http://fallback.org/'
JSONLD_OPTIONS = {'algorithm': 'URDNA2015', 'format': 'application/nquads'}
FALLBACK_CONTEXT = {'@vocab': FALLBACK_VOCAB}

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
SCHEMA_FILE_V1_1 = os.path.join(BASE_DIR, 'schema/1.1/certificate-schema-v1-1.json')
SCHEMA_FILE_V1_2 = os.path.join(BASE_DIR, 'schema/1.2/blockchain-certificate-1.2.json')
SCHEMA_UNSIGNED_FILE_V1_2 = os.path.join(BASE_DIR, 'schema/1.2/certificate-document-1.2.json')
JSON_LD_CONTEXT_V1_2 = os.path.join(BASE_DIR, 'schema/1.2/context.json')
SCHEMA_UNSIGNED_FILE_V1_2 = os.path.join(BASE_DIR, 'schema/1.2/certificate-document-1.2.json')


class BlockcertValidationError(Exception):
    pass


def validate_v1_1(certificate_json):
    """
    Propagates BlockcertValidationError on failure
    :param certificate_json:
    :return:
    """

    with open(SCHEMA_FILE_V1_1) as schema_f:
        schema_json = json.load(schema_f)
        return validate_json(certificate_json, schema_json)


def validate_v1_2(certificate_json):
    """
    Propagates BlockcertValidationError on failure
    :param certificate_json:
    :return:
    """

    with open(SCHEMA_FILE_V1_2) as schema_f:
        schema_json = json.load(schema_f)
        return validate_json(certificate_json, schema_json)


def validate_v2(certificate_json):
    response = urlopen(BLOCKCERTS_V2_SCHEMA)
    schema_v2_bytes = response.read()
    schema_v2 = json.loads(schema_v2_bytes.decode('utf-8'))
    result = validate_json(certificate_json, schema_v2)
    try:
        response.close()
    except:
        logging.warning('exception trying to close...')
        # doesn't exist in python2
        pass
    return result


def validate_unsigned_v1_2(certificate_json):
    """
    Raises or propagates BlockcertValidationError on failure
    :param certificate_json:
    :return:
    """
    with open(SCHEMA_UNSIGNED_FILE_V1_2) as schema_f:
        schema_json = json.load(schema_f)
        # first a conditional check not done in the json schema
        if certificate_json['recipient']['hashed'] and not certificate_json['recipient']['salt']:
            logging.error('certificate is hashed but has no salt')
            raise jsonschema.exceptions.ValidationError('certificate is hashed but has no salt')

        return validate_json(certificate_json, schema_json)


def validate_json(certificate_json, schema_json):
    """
    If no exception is raised, the instance is valid. Raises BlockcertValidationError is validation fails.
    :param certificate_json:
    :param schema_json:
    :return:
    """
    try:
        jsonschema.validate(certificate_json, schema_json)
        return True
    except jsonschema.exceptions.ValidationError as ve:
        logging.error(ve, exc_info=True)
        raise BlockcertValidationError(ve)


def validate(data_file, schema_file):
    with open(data_file) as data_f, open(schema_file) as schema_f:
        data = json.load(data_f)
        schema = json.load(schema_f)
        return validate_json(data, schema)


def compact_with_json_ld_context(input_json, document_loader=None):
    options = {}
    if document_loader:
        options['documentLoader'] = document_loader
    with open(JSON_LD_CONTEXT_V1_2) as context_f:
        ctx = json.load(context_f)
        compacted = jsonld.compact(input_json, ctx, options=options)
        return compacted


def normalize_jsonld(json_ld_to_normalize, document_loader=None, detect_unmapped_fields=False):
    """
    Canonicalize the JSON-LD certificate.

    The detect_unmapped_fields parameter is a temporary, incomplete, workaround to detecting fields that do not
    correspond to items in the JSON-LD schemas. It works in the Blockcerts context because:
    - Blockcerts doesn't use a default vocab
    - fallback.org is not expected to occur

    Because unmapped fields get dropped during canonicalization, this uses a trick of adding
     {"@vocab": "http://fallback.org/"} to the json ld, which will cause any unmapped fields to be prefixed with
     http://fallback.org/.

    This issue will be addressed in a first-class manner in the future.

    :param json_ld_to_normalize:
    :param detect_unmapped_fields:
    :return:
    """
    json_ld = json_ld_to_normalize
    options = deepcopy(JSONLD_OPTIONS)
    if document_loader:
        options['documentLoader'] = document_loader

    if detect_unmapped_fields:
        json_ld = deepcopy(json_ld_to_normalize)
        prev_context = JsonLdProcessor.get_values(json_ld_to_normalize, '@context')
        prev_context.append(FALLBACK_CONTEXT)
        json_ld['@context'] = prev_context

    normalized = jsonld.normalize(json_ld, options=options)

    if detect_unmapped_fields and FALLBACK_VOCAB in normalized:
        unmapped_fields = []
        for m in re.finditer('<http://fallback\.org/(.*)>', normalized):
            unmapped_fields.append(m.group(0))
        error_string = ', '.join(unmapped_fields)
        raise BlockcertValidationError(
            'There are some fields in the certificate that do not correspond to the expected schema. This has likely been tampered with. Unmapped fields are: ' + error_string)
    return normalized


def _parse_json_ld(filename, document_loader=None):
    # just some experiments
    options = {}
    if document_loader:
        options['documentLoader'] = document_loader
    with open(filename) as data_f:
        data = json.load(data_f)
        compacted = compact_with_json_ld_context(data, document_loader)
        expanded = jsonld.expand(compacted, options=options)
        options = {'algorithm': 'URDNA2015', 'format': 'application/nquads'}
        if document_loader:
            options['documentLoader'] = document_loader
        normalized = jsonld.normalize(data, options)
        print(json.dumps(expanded, indent=2))


if __name__ == '__main__':
    valid = validate('../../examples/1.1/sample_unsigned_cert-1.1.json',
                     '../schema/1.1/certificate-schema-v1-1.json')
    print('certificate is valid? ' + str(valid))

    valid = validate('../../examples/1.1/sample_signed_cert-1.1.json',
                     '../schema/1.1/certificate-schema-v1-1.json')
    print('certificate is valid? ' + str(valid))

    # valid = validate('../../examples/1.2/sample_unsigned_cert-1.2.json',
    #                 '../schema/1.2/digital-certificate-1.2.json')
    # print('certificate is valid? ' + str(valid))

    valid = validate('../../examples/1.2/sample_signed_cert-1.2.json',
                     '../schema/1.2/blockchain-certificate-1.2.json')
    print('certificate is valid? ' + str(valid))

    _parse_json_ld('../../examples/1.2/sample_signed_cert-1.2.json')
