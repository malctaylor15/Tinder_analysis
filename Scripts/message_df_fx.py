# This script has functions used in the EDA for the tinder analysis

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# import json
# import os

from Scripts import utils

def word_list_in_phrase(word_list, phrase, partial = False):
    """
    Check if word is in phrase list -- comparing 2 lists
    << use sets instead? >>

    word_list (list) : list of strings that one or more may be in phrase
    phrase (str): sentence list string that will be split by ' '

    """

    # Normalize phrase
    phrase_list = phrase.split(" ")
    phrase_list = set([x.lower() for x in phrase_list])

    # Compare
    # Use sets instead
    result = 0
    if partial == True: # partial flag, if word in any part of any word
        for word in word_list:
            for phrase_part in phrase_list:
                if word in phrase_part:
                    result = word
                # result += 1 if word in phrase_part else 0
        # result = 1 if result > 0 else 0
        return result

    else:
        word_list= set(word_list)
        common_words = phrase_list.intersection(word_list)
        if len(common_words) > 0:
            return 1
        else:
            return 0



def get_msg_df(message_dict):

    """
    Parse the message dictionary for each conversation -- creates 2 level index of match_id and message within convo number
    The message dict should have the match_id and the list of messages (your side)

    Input:
        message_dict (dict): raw messages from json
    Output:
        message_df (pd.DataFrame): message data frame with columns to find key attributes
    """

    match_id = message_dict['match_id']
    message_list = message_dict['messages']

    message_df = pd.DataFrame(message_list)
    schema = {'fixed_height', 'from', 'message', 'sent_date', 'to', 'type'}

    # Add in columns not present, fill in with na
    message_df = pd.DataFrame(message_list)
    schema = {'fixed_height', 'from', 'message', 'sent_date', 'to', 'type'}
    for col in schema:
        if col not in message_df.columns:
            message_df[col] = np.nan

    # Set the heirarchical index
    new_index_tups = [(match_id, msg_num) for msg_num in message_df.index.values]
    new_index = pd.MultiIndex.from_tuples(new_index_tups, names = ["match_id", "msg_number"])
    message_df.index = new_index

    # If there are no messages, add in one with index of -1
    if message_df.shape[0] == 0:
        other_final_cols = ["n_words_in_msg", "time_since_last_msg"\
        , "time_since_last_2_msgs", "funny_word_in_msg", "funny_word_in_msg"]
        for col in other_final_cols:
            if col not in message_df.columns:
                message_df[col] = np.nan
        message_df.loc[(match_id, -1), :] = np.nan
        return(message_df)


    # Check schema
    mismatches = set(message_df.columns).symmetric_difference(schema)
    if mismatches != set():
        print("Data schema mismatch in message df!")
        print(mismatches)
        raise ValueError()

    # Reformat sent date
    message_df['sent_date'] = pd.to_datetime(message_df['sent_date'])

    # Make new columns about message
    message_df["n_words_in_msg"]=message_df.apply(lambda x: len(x['message'].split(" ")), axis = 1)


    # New column about time between messages
    message_df['time_since_last_msg'] = message_df['sent_date'].diff()
    message_df['time_since_last_2_msgs'] = message_df['sent_date'].diff(2)
    # Think about escalation in message sending or if time between texts is small then...

    # Check for key words
    funny_words = ["hahaha", "lol", "haha", "ha"]
    message_df['funny_word_in_msg'] = message_df.apply(lambda x: word_list_in_phrase(funny_words, x['message']), axis =1 )

    question_words = ["who", "what", "where", "when", "why", "how", "how's", "what's"]
    message_df['question_word_in_msg'] = message_df.apply(lambda x: word_list_in_phrase(question_words, x['message']), axis =1 )
    message_df['question_mark_in_msg'] = message_df.apply(lambda x: 1 if "?" in x['message'] else 0, axis = 1)
    message_df['exclamation_mark_in_msg'] = message_df.apply(lambda x: 1 if "!" in x['message'] else 0, axis=1)

    explicit_words = ["fuck", "shit", "bitch", "sex", "ass"]
    message_df["explicit_word_in_msg"] = message_df.apply(
        lambda x: word_list_in_phrase(explicit_words, x['message']), axis =1 )



    return(message_df)


def flatten_date(timestamp):
    """
    Flatten time stamp date into month and year string
    Used to help create groupbys
    Best used in apply loops

    """
    yr_raw = timestamp.year
    yr = str(yr_raw)
    mon_raw = timestamp.month
    if mon_raw < 10:
        mon = "0"+str(mon_raw)
    else:
        mon = str(mon_raw)

    flatten_date = yr+mon
    return(flatten_date)

def plot_number_of_msgs_ovr_time(flg_ovr_time):
    """
    Plot number of messags over time
    """

    fig, ax = plt.subplots(1)
    ax.plot(flg_ovr_time)
    fig.suptitle("Number of messages per month")
    ax.set_xlabel("Year + Month")
    ax.set_ylabel("Number of Occurances")
    ax.grid(True)
    # Show every n (3rd) label on x axis
    n = 3
    for index, label in enumerate(ax.xaxis.get_ticklabels()):
        if index % n != 0:
            label.set_visible(False)
    fig.autofmt_xdate()
    return(fig)


def plot_flag_fx(n_msg_over_time, flg_ovr_time, demo_flg):
    """
    Plots the number of messages vs time and a flag over time

    n_msg_over_time (Series): number of message over time
        The index should be the same as the flg_ovr_time

    flg_ovr_time (Series): count of the flag over time

    demo_flg (str): Name of the flag-- will be marked in the legend
    """

    fig, ax = plt.subplots(1)
    ax.plot(n_msg_over_time, label = "Number of messages")
    ax.plot(flg_ovr_time, label = demo_flg)
    fig.suptitle("Number of " + demo_flg + " per month")
    ax.set_xlabel("Year + Month")
    ax.set_ylabel("Number of Occurances")
    ax.grid(True)
    # Show every n (3rd) label on x axis
    n = 3
    for index, label in enumerate(ax.xaxis.get_ticklabels()):
        if index % n != 0:
            label.set_visible(False)
    fig.autofmt_xdate()
    leg = ax.legend(loc='best', fancybox=True)
    return(fig)

def get_msg_related_plots(all_msg_df):
    """
    Main work flow for gathering plots related to messages

    :return:
    """

    # Data preparation for plots
    all_msg_df['flatten_date'] = all_msg_df['sent_date'].apply(flatten_date)
    dt_gb = all_msg_df.groupby('flatten_date')
    flag_col = ['explicit_word_in_msg', 'funny_word_in_msg', 'question_mark_in_msg', 'question_word_in_msg', "exclamation_mark_in_msg"]
    n_msg_over_time = dt_gb.apply(len)

    # Create plots of message over time with flags
    plts = []
    plts.append(plot_number_of_msgs_ovr_time(n_msg_over_time))
    for demo_flg in flag_col:
        plts.append(plot_flag_fx(n_msg_over_time, dt_gb[demo_flg].sum(), demo_flg))

    return(plts)


def get_message_metrics(message_df):
    """
    Get metrics from message dataframe

    message_df (pandas DataFrame):
        Dataframe with info about messages sent, time, content of message, and whom it was sent

    Returns
    metrics_to_save (dict):
        dictionary of name of metric and value
    """

    # Input Validation
    expected_columns = ['sent_date', 'n_words_in_msg', 'message']
    for col in expected_columns:
        if col not in message_df.columns:
            raise IndexError(col + " not in dataframe columns " + message_df.columns)

    expected_index_keys = ['match_id', 'msg_number']
    for col in expected_index_keys:
        if col not in message_df.index.names:
            raise IndexError(col + " not in dataframe columns " + message_df.index.names)

    # Set up -- needed for multi index slicing
    idx = pd.IndexSlice

    # Metrics to save
    metrics_to_save = {}
    metrics_to_save["Date of First Message Sent"] = message_df['sent_date'].min().strftime('%b %d %Y')
    metrics_to_save["Date of Last Message Sent"] = message_df['sent_date'].max().strftime('%b %d %Y')
    metrics_to_save["Number of Matches"] = message_df.index.get_level_values('match_id').nunique()
    metrics_to_save["Number Matches with no Messages"] = message_df.loc[idx[:, -1],].shape[0]
    metrics_to_save["Most Number of Messages Sent to a Match"] = message_df.index.get_level_values('msg_number').max()
    metrics_to_save["Average Number of Words per Message"] = message_df['n_words_in_msg'].mean().round(2)
    metrics_to_save["Median Number of Words per Message"] = np.round(message_df['n_words_in_msg'].quantile(0.50), 2)
    # metrics_to_save["Average Messages Per Match"] = message_df.index.get_level_values('msg_number').mean().round(3)

    # Time calculations
    time_diff_days = (message_df['sent_date'].max() - message_df['sent_date'].min()).days
    years = int(time_diff_days / 365)
    months = int((time_diff_days % 365) / 30)
    days = (time_diff_days % 365) % 30
    metrics_to_save["Total Time on Tinder from First Message to Last"] = "{} years {} months {} days" \
        .format(years, months, days)

    # First message analysis
    first_msg = message_df.loc[idx[:, 0], "message"]
    first_msg = pd.DataFrame(first_msg)

    # Clean and generate additional flags
    first_msg['message'] = first_msg['message'].str.rstrip(' ')
    first_msg['message'] = first_msg['message'].str.rstrip('  ')
    same_first_message = first_msg['message'].value_counts().sort_values(ascending=False)

    first_msg['hey_hi_flag'] = first_msg['message'].str.count('((H|h)ey|(H|h)i)')
    first_msg['How \'sit going_flag'] = first_msg['message'].str.contains('it going')

    # Save some metrics
    metrics_to_save["Hey or Hi in First Message"] = first_msg['hey_hi_flag'].sum()
    metrics_to_save["(How's ) it going in First Message"] = first_msg['How \'sit going_flag'].sum()
    metrics_to_save["Most Common First Message"] = same_first_message.index[0]
    metrics_to_save["Number of Times Most Common First Message Used"] = same_first_message[0]
    metrics_to_save["Second Most Common First Message"] = same_first_message.index[1]
    metrics_to_save["Number of Times Second Most Common First Message Used"] = same_first_message[1]
    metrics_to_save["Third Most Common First Message"] = same_first_message.index[2]
    metrics_to_save["Number of Times Third Most Common First Message Used"] = same_first_message[2]

    metrics_to_save = utils.check_dict_types(metrics_to_save)
    return (metrics_to_save)
