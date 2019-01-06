zip -g aws_transformer.zip aws_transformer.py
zip -g -r aws_transformer.zip Scripts
aws s3 cp aws_transformer.zip s3://demo-tinder-data

aws lambda update-function-code --function-name tinder_pdf --s3-bucket demo-tinder-data --s3-key aws_transformer.zip
aws lambda invoke --function-name tinder_pdf --invocation-type Event --payload file://inputfile.txt outfile.txt
echo "Completed aws test"
