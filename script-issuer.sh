#!/bin/bash

source venv3/bin/activate
cd cert-issuer
python3 issue_certificates.py -c confx.ini
cp -r /Users/carlavega/Documents/Proyecto/cert-issuer/data/blockchain_certificates/* /Users/carlavega/Documents/Proyecto/cert-viewer/cert_data/
deactivate
