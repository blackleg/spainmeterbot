#!/bin/bash
echo "- Deploy Script"
echo "-- Decrypt ssh key"
openssl aes-256-cbc -K $encrypted_0b3c30bbe660_key -iv $encrypted_0b3c30bbe660_iv -in .travis/deploy_rsa.enc -out deploy_rsa -d
echo "-- Launch ssh agent"
eval "$(ssh-agent -s)"
sleep 5
echo "-- Add ssh key"
chmod 600 deploy_rsa
ssh-add deploy_rsa
sleep 5
echo "-- Deploy scripts"
## Deploy requirements
rsync -r  "$TRAVIS_BUILD_DIR/requirements.txt" "$deployurl/requirements.txt"
## Deploy scripts
rsync -r   "$TRAVIS_BUILD_DIR/demand.py" "$deployurl/demand.py"
rsync -r   "$TRAVIS_BUILD_DIR/production.py" "$deployurl/production.py"
rsync -r   "$TRAVIS_BUILD_DIR/production_balearic_islands.py" "$deployurl/production_balearic_islands.py"
echo "-- Scripts deployed"