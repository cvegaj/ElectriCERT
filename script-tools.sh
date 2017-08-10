#!/bin/bash

cd cert-tools
mv ../cert-tools/sample_data/unsigned_certificates/* ../cert-tools/sample_data/backup/
create-certificate-template -c confx.ini
instantiate-certificate-batch -c confx.ini
cp -r ../cert-tools/sample_data/unsigned_certificates/* ../cert-issuer/data/unsigned_certificates/
