
import pandas as pd
# import numpy as np
import matplotlib.pyplot as plt
import json

from Scripts import EDA_functions as mt_eda
from matplotlib.backends.backend_pdf import PdfPages
import sys
import uuid
import boto3
# from collections import Counter
import os
# import re

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

    # Open JSON file
    with open(data_path, "r") as inp:
        data = json.load(inp)

    # Parse Json and put into dataframe with levels of MatchId and message number
    msg_df = pd.DataFrame(data['Messages'][10]['messages'])
    msg_df['sent_date'] = pd.to_datetime(msg_df['sent_date'])
    list_of_dfs = [mt_eda.get_msg_df(msg_dict) for msg_dict in data["Messages"]]
    all_msg_df = pd.concat(list_of_dfs, axis=0)

    # Data preparation for plots
    all_msg_df['flatten_date'] = all_msg_df['sent_date'].apply(mt_eda.flatten_date)
    dt_gb = all_msg_df.groupby('flatten_date')
    flag_col = ['explicit_word_in_msg', 'funny_word_in_msg', 'question_mark_in_msg', 'question_word_in_msg']
    n_msg_over_time = dt_gb.apply(len)

    # Create plots of message over time with flags
    plts = []
    plts.append(mt_eda.plot_number_of_msgs_ovr_time(n_msg_over_time))
    for demo_flg in flag_col:
        plts.append(mt_eda.plot_flag_fx(n_msg_over_time, dt_gb[demo_flg].sum(), demo_flg))

    # Export plots to pdf
    pp = PdfPages(output_path)
    for plt in plts:
        pp.savefig(plt)
    pp.close()

    print("Complete!")
    return(0)


def handler(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        download_path = u'/tmp/data'
        upload_path = '/tmp/{}_output_graphs.pdf'.format(key)

        s3_client.download_file(bucket, key, download_path)
        parse_json(download_path, upload_path)
        s3_client.upload_file(upload_path, bucket, key)

    return (0)