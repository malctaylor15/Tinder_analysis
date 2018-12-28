
import pandas as pd
# import numpy as np
import matplotlib.pyplot as plt
import json

from Scripts import EDA_functions as mt_eda
from matplotlib.backends.backend_pdf import PdfPages
import sys
# from collections import Counter
# import os
# import re


def parse_json(data_path, pdf_name= "output_graphs.pdf"):
    """
    Parses JSON, creates pdf of several plots

    :param data_path: string for location of the json file
    :param pdf_name: (optional) string for the name and location for the pdf that was created
    :return:
    """


    # Open JSON file
    with open(data_path, "rb") as inp:
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
    pp = PdfPages(pdf_name)
    for plt in plts:
        pp.savefig(plt)
    pp.close()

    print("Complete!")
    return(0)

if __name__ == "__main__":
    path = sys.argv[1]
    parse_json(path)