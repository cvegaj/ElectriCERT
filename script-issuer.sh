#!/bin/bash

echo "Moving old blockchain_certificates to backup folder..."
mv ./cert-issuer/data/blockchain_certificates/* ./cert-issuer/data/backup/blockchain_certificates/
echo "Activating virtual enviroment..."
source venv3/bin/activate
cd cert-issuer
python3 issue_certificates.py -c confx.ini
echo "Moving blockchain_certificates to cert-data folder..."
cp -r ../cert-issuer/data/blockchain_certificates/* ../cert-viewer/cert_data/
echo "Moving processed unsigned_certificates to backup folder..."
mv ../cert-issuer/data/unsigned_certificates/* ../cert-issuer/data/backup/unsigned_certificates/
deactivate
