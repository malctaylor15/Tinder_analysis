#!/usr/bin/env bash
# Zips python environment, adds scripts, uploads zip to s3, update lambda function, run test case
source ~/Tinder_env/bin/activate
cd /home/owner/Tinder_env/lib/python3.6/site-packages/
zip -r9 /home/owner/Documents/Github_projects/Tinder_analysis/aws_transformer.zip . -q
cd $git_path/Tinder_analysis/
zip -g aws_transformer.zip aws_transformer.py
zip -g -r aws_transformer.zip Scriptspip
echo "Zip created"
aws s3 cp aws_transformer.zip s3://demo-tinder-data
aws lambda update-function-code --function-name CreateTinderPDF --s3-bucket demo-tinder-data --s3-key aws_transformer.zip
aws lambda invoke --function-name CreateTinderPDF --invocation-type Event --payload file://inputfile.txt outfile.txt
echo "Completed aws test"
