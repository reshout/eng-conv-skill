#!/bin/bash

echo "##### creating lambda.zip #####"
zip lambda.zip main.py conv.json

echo "##### uploading lambda.zip #####"
aws lambda update-function-code \
    --function-name eng-conv-skill \
    --profile reshout \
    --zip-file fileb://lambda.zip

echo "##### deleting lambda.zip #####"
rm lambda.zip
