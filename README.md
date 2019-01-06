# Tinder_analysis
Explore My Tinder Data  

In this repository, I am beginning to examine Tinder available from my Tinder profile. We are able to receive **our** side of the conversation for your past matches.  

We are able to conduct some light analysis on the conversations to understand how the app has been used over time.  

As of 12/12/2018, the plan is to create a web app to enable a user to upload the json from Tinder and download a pdf to learn something about their Tinder usage.  


## Download your Tinder Data  

Tinder allows users to download some of their data that is stored with on the servers. You can begin by going [here](https://account.gotinder.com/data). You will receive an email that the file will be available for download within 3 days (mine came on the 3rd day) with only 24 hours to download before the link expires.  

After you download the zip file, there should be 3 items: an index.html, a folder called your_photos, and a file called data.json. The index_html reads the data.json and provides several tabs and makes some of the raw data more readable. It is worth poking through the index html to browse the data to ensure it is what you expect it to be.  

I intend for the app to use the data.json file. The json will have all the same content as the local webpage.



## AWS Integration

Part of the plan is to allow a user to upload their data.json from Tinder and download a PDF of some metrics about their usage and other information.

To accomplish this goal, I plan on using Amazon Web Services and the serverless paradigm.

As of 12/31/2018, I have pacakges up the python dependencies (numpy, pandas, matplotlib) and the source codes (EDA_functions and aws_transformer.py) into a zip that will work with AWS lambda. Thus far the backend side works well -- it can read a json from s3 and produces a pdf with the analysis to s3. I plan to expose these end points and allow any user with their Tinder data in a json format to have access to this analysis.

### Files  

Below is a quick guide to some of the files in the directory.

* inputfile.txt -- AWS test script -- mimics post request to the s3 bucket -- after the post request the lambda function should be triggered which should create the pdf

* aws_transformer -- main python script that calls scripts in the Scripts folder -- handles the aws main function, the command line main function and basic parsing of the json

* EDA notebooks -- first passes at looking at the data-- most functions in the notebook were updated after transfer to aws_transformer

* zip_env_test_lambda.sh, update_transformer.sh  -- bash scripts to help automate the testing process -- reveal some of the backend work -- note there are hard references to paths on my computer and s3 buckets so it will most likely not work for you

### Resources  

Two resources from AWS that have helped building the AWS pipeline
1. [Tutorial using S3 and Lambda](https://docs.aws.amazon.com/lambda/latest/dg/with-s3-example.html)
2. [Python code for the tutorial](https://docs.aws.amazon.com/lambda/latest/dg/with-s3-example-deployment-pkg.html#with-s3-example-deployment-pkg-python)
