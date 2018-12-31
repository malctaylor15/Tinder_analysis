
## AWS Integration

Part of the plan is to allow a user to upload their data.json from Tinder and download a PDF of some metrics about their usage and other information. 

To accomplish this goal, I plan on using Amazon Web Services and the serverless paradigm. 

As of 12/31/2018, I have pacakges up the python dependencies (numpy, pandas, matplotlib) and the source codes (EDA_functions and aws_transformer.py) into a zip that will work with AWS lambda. Thus far the backend side works well -- it can read a json from s3 and produces a pdf with the analysis to s3. I plan to expose these end points and allow any user with their Tinder data in a json format to have access to this analysis. 

### Files  
There are several files including a few bash scripts that I made to help automate some of the creation of the package, uploading to aws s3 and updating the aws lambda function. There are some hard coded paths that are specifically referenced to my computer so it will not work for everyone. They can provide some insight into some of the backend steps. 

### Resources  

Two resouces from AWS that have helped are 
1. [Tutorial using S3 and Lambda](https://docs.aws.amazon.com/lambda/latest/dg/with-s3-example.html)
2. [Python code for the tutorial](https://docs.aws.amazon.com/lambda/latest/dg/with-s3-example-deployment-pkg.html#with-s3-example-deployment-pkg-python) 

