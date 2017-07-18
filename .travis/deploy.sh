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
rsync -r --delete-after --quiet --exclude '.env' --exclude 'spainmeter.log' $TRAVIS_BUILD_DIR/ "$deployurl"