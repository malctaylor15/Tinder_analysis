# Tinder_analysis

In this repository, I am beginning to examine Tinder available from my Tinder profile. Tinder gives us access to various pieces of information from the profile including App Usage and **our** side of the conversation  since profile creation. After conducting some EDA on each of the sections, I've created a few graphs to visual some of the trends over time and several other metrics. 

## Stages of Development 

The initial plan was to model this project in the [severless stack framework](https://serverless-stack.com/). The serverless stack framework consists of a react frontend and an AWS lambda backend. I built the backend lambda functions to create the pdf's if the file from Tinder was uploaded to a certain bucket. 

I have recently shifted to using dash and flask as the web framework for the dashboards. Dash is a python framework for building dashboards. More information about Dash can be found [here](https://dash.plot.ly/) More information about the dash notebooks that describe my Tinder data can be found [here](https://github.com/malctaylor15/Tinder_dash)


## AWS Integration

Part of the functionality was to allow a user to upload their data.json/ zip file  from Tinder and download a PDF of some metrics about their usage and other information.

I have pacakged the python dependencies (numpy, pandas, matplotlib) and the source codes (EDA_functions and aws_transformer.py) into a zip that will work with AWS lambda. Thus far the lambda functions and backend work well -- it can read a json from s3 and produces a pdf with the analysis to s3. I plan to expose these end points and allow any user with their Tinder data in a json format to have access to this analysis.

### Files  

Below is a quick guide to some of the files in the directory.

* inputfile.txt -- AWS test script -- mimics post request to the s3 bucket -- after the post request the lambda function should be triggered which should create the pdf

* aws_transformer -- main python script that calls scripts in the Scripts folder -- handles the aws main function, the command line main function and basic parsing of the json

* EDA notebooks -- first passes at looking at the data-- most functions in the notebook were updated after transfer to aws_transformer

* zip_env_test_lambda.sh, update_transformer.sh  -- bash scripts to help automate the testing process -- reveal some of the backend work -- note there are hard references to paths on my computer and s3 buckets so it will most likely not work for you


## Download your Tinder Data  

Tinder allows users to download some of their data that is stored with on the servers. You can begin by going [here](https://account.gotinder.com/data). You will receive an email that the file will be available for download within 3 days (mine came on the 3rd day) with only 24 hours to download before the link expires.  

After you download the zip file, there should be 3 items: an index.html, a folder called your_photos, and a file called data.json. The index_html reads the data.json and provides several tabs and makes some of the raw data more readable. It is worth poking through the index html to browse the data to ensure it is what you expect it to be.  


### Resources  

Two resources from AWS that have helped building the AWS pipeline
1. [Tutorial using S3 and Lambda](https://docs.aws.amazon.com/lambda/latest/dg/with-s3-example.html)
2. [Python code for the tutorial](https://docs.aws.amazon.com/lambda/latest/dg/with-s3-example-deployment-pkg.html#with-s3-example-deployment-pkg-python)
