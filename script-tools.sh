#!/bin/bash

cd cert-tools
cp -r /Users/carlavega/Documents/Proyecto/cert-tools/sample_data/unsigned_certificates/* /Users/carlavega/Documents/Proyecto/cert-tools/sample_data/backup/
create-certificate-template -c confx.ini
instantiate-certificate-batch -c confx.ini
cp -r /Users/carlavega/Documents/Proyecto/cert-tools/sample_data/unsigned_certificates/* /Users/carlavega/Documents/Proyecto/cert-issuer/data/unsigned_certificates/
