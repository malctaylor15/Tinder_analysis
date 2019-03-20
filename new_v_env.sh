#!/usr/bin/env bash
virtualenv parse_env
source ~/parse_env/bin/activate

aws lambda add-permission --function-name tinder_handle_raw_upload --principal s3.amazonaws.com \
--statement-id id1234 --action "lambda:InvokeFunction" \
--source-arn arn:aws:s3:::tinder-data-prod \
--source-account 615178312602

aws lambda add-permission --function-name tinder_pdf --principal s3.amazonaws.com \
--statement-id id12455 --action "lambda:InvokeFunction" \
--source-arn arn:aws:s3:::tinder-data-prod \
--source-account 615178312602

aws lambda add-permission --function-name CreateTinderPDF --principal s3.amazonaws.com \
--statement-id 1233345 --action "lambda:InvokeFunction" \
--source-arn arn:aws:s3:::tinder-data-prod \
--source-account 615178312602


# Check
aws lambda get-policy --function-name tinder_pdf
