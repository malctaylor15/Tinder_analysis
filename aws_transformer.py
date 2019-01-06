
import pandas as pd
# import numpy as np
import matplotlib.pyplot as plt
import json

from matplotlib.backends.backend_pdf import PdfPages
import sys
import uuid
import boto3
# from collections import Counter
import os
import sys
# import re
import pdb

from Scripts import EDA_functions as mt_eda
from Scripts import usage_analysis_fx as usage


s3_client = boto3.client('s3')

def parse_json(data_path, output_path= "output_graphs.pdf"):
    """
    Parses JSON, creates pdf of several plots

    :param data_path: string for location of the json file
    :param pdf_name: (optional) string for the name and location for the pdf that was created
    :return:
    """
    print(data_path)
    if not os.path.isfile(data_path):
        print("File not found at ", data_path)
        return(1)
    # pdb.set_trace()
    # Open JSON file
    with open(data_path, 'rb') as inp:
        data = json.load(inp)

    # Parse Json and put into dataframe with levels of MatchId and message number
    list_of_dfs = [mt_eda.get_msg_df(msg_dict) for msg_dict in data["Messages"]]
    all_msg_df = pd.concat(list_of_dfs, axis=0)

    # Get plots related to messages
    msg_plots = mt_eda.get_msg_related_plots(all_msg_df)

    # Gather data for usage plots
    usage_df = pd.DataFrame(data["Usage"])
    usage_plots = usage.create_usage_plots(usage_df)

    # Export plots to pdf
    pp = PdfPages(output_path)
    for tmp_plt in msg_plots:
        pp.savefig(tmp_plt)

    for tmp_plt in usage_plots:
        pp.savefig(tmp_plt)

    pp.close()
    print("Completed parse json!")

    return(0)


def handler(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        download_path = str('/tmp/data_{}.json'.format(uuid.uuid4()))
        upload_path = str('/tmp/{}_output_graphs.pdf'.format(key))
        new_key = "output_graphs.pdf"

        s3_client.download_file(bucket, key, download_path)
        parse_json(download_path, upload_path)
        s3_client.upload_file(upload_path, bucket, new_key)
        print("Finished uploading PDF to s3")

    return (0)


if __name__ =="__main__":
    input = sys.argv[1]
    with open(input, "rb") as inp:
        test_event = json.load(inp)
    handler(test_event, None)
    print("Completed python main fx")

# To test run:
# python aws_transformer.py inputfile.txt
