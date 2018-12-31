zip -g aws_transformer.zip aws_transformer.py

aws s3 cp aws_transformer.zip s3://demo-tinder-data 

aws lambda update-function-code --function-name tinder_pdf --s3-bucket demo-tinder-data --s3-key aws_transformer.zip

