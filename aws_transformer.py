
import pandas as pd
# import numpy as np
import matplotlib.pyplot as plt
plt.ioff()
import json

from matplotlib.backends.backend_pdf import PdfPages
import sys
import uuid
import boto3
# from collections import Counter
import os
import sys
import datetime
# import re
import pdb
from decimal import Decimal


from Scripts import utils
from Scripts import message_df_fx as msg_fx
from Scripts import usage_analysis_fx as usage
from Scripts import user_page_fx as user

s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('TinderAnalysis')

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
    # Open JSON file
    with open(data_path, 'rb') as inp:
        data = json.load(inp)

    # Parse Json and put into dataframe with levels of MatchId and message number
    list_of_dfs = [msg_fx.get_msg_df(msg_dict) for msg_dict in data["Messages"]]
    all_msg_df = pd.concat(list_of_dfs, axis=0, sort = True)

    # Get plots related to messages
    msg_plots = msg_fx.get_msg_related_plots(all_msg_df)
    msg_metrics = msg_fx.get_message_metrics(all_msg_df)

    # Gather data for usage plots
    usage_df = pd.DataFrame(data["Usage"])
    usage_plots = usage.create_usage_plots(usage_df)
    usage_metrics = usage.gather_usage_stats(usage_df)

    # Gather user info to keep
    user_df = user.get_userdf_parts(data["User"])

    # Combine metrics to be stored
    all_metrics = {}
    all_metrics["usage"] = usage_metrics
    all_metrics["message"] = msg_metrics
    all_metrics["user"] = user_df

    for metric_type in all_metrics.keys():
        if type(all_metrics[metric_type]) == dict:
            for key in all_metrics[metric_type].keys():
                if (type(all_metrics[metric_type]) == pd.DataFrame) or \
                    (type(all_metrics[metric_type][key]) == pd.Series):
                    all_metrics[metric_type][key] = all_metrics[metric_type][key].to_dict()


    # Export plots to pdf
    pp = PdfPages(output_path)
    for tmp_plt in msg_plots:
        pp.savefig(tmp_plt)

    for tmp_plt in usage_plots:
        pp.savefig(tmp_plt)

    pp.close()
    print("Completed parse json!")

    return(all_metrics)



def handler(event, context):

    for record in event['Records']:
        uuid_key = uuid.uuid4()
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        download_path = str('/tmp/data_{}.json'.format(uuid_key))
        upload_path = str('/tmp/{}_output_graphs.pdf'.format(uuid_key))


        s3_client.download_file(bucket, key, download_path)
        metrics = parse_json(download_path, upload_path)

        unique_id = "_".join([metrics['user']['create_date'],
                              metrics['user']['birth_date']])

        new_key = 'graphs/output_graphs_' + unique_id + '.pdf'

        tbl_response = table.put_item(
            Item = {
                'created_birthday': unique_id,
                'request_date': str(datetime.datetime.now()),
                'pdf_s3_bucket': bucket,
                'pdf_s3_file_name': new_key,
                'user_df': metrics['user'],
                'usage_df': metrics['usage'],
                'message_df':metrics['message']
            }
        )

        # TODO: Add call back to parse server responses
        s3_client.upload_file(upload_path, bucket, new_key)
        print("Finished uploading PDF to s3 and data base entry attempted")



    return (0)


if __name__ =="__main__":
    input = sys.argv[1]
    with open(input, "rb") as inp:
        test_event = json.load(inp)
    handler(test_event, None)
    print("Completed python main fx")

# To test run:
# python aws_transformer.py inputfile.txt
