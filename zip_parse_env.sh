#!/usr/bin/env bash

# Zips python environment, adds scripts, uploads zip to s3, update lambda function, run test case
source ~/parse_env/bin/activate
cd /home/owner/parse_env/lib/python3.6/site-packages/
zip -r9 /home/owner/Documents/Github_projects/Tinder_analysis/parse_env.zip . -q
cd $git_path/Tinder_analysis/
zip -g parse_env.zip handle_upload.py
echo "Parse Env Zip created"
aws s3 cp parse_env.zip s3://demo-tinder-data
aws lambda update-function-code --function-name tinder_handle_raw_upload --s3-bucket demo-tinder-data --s3-key parse_env.zip
aws lambda invoke --function-name tinder_handle_raw_upload --invocation-type Event --payload file://inputfile.txt outfile.txt
echo "Completed aws test"
