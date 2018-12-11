# This script has functions used in the EDA for the tinder analysis

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import os


def word_list_in_phrase(word_list, phrase):
    """
    Check if word is in phrase list -- comparing 2 lists
    << use sets instead? >>

    word_list (list) : list of strings that one or more may be in phrase
    phrase (str): sentence list string that will be split by ' '

    """

    # Normalize phrase
    phrase_list = phrase.split(" ")
    phrase_list = [x.lower() for x in phrase_list]

    # Compare
    for word in word_list:
        if word in phrase_list:
            return 1
    return 0



def get_msg_df(message_dict):

    """
    Parse the message dictionary for each conversation
    The message dict should have the match_id and the list of messages (your side)


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

    # If there are no messages, add in one with index of -1
    if message_df.shape[0] == 0:
        other_final_cols = ["n_words_in_msg", "time_since_last_msg"\
        , "time_since_last_2_msgs", "funny_word_in_msg", "funny_word_in_msg"]
        for col in other_final_cols:
            if col not in message_df.columns:
                message_df[col] = np.nan
        message_df.loc[match_id, -1] = np.nan
        return(message_df)

    # Check schema
    mismatches = set(message_df.columns).symmetric_difference(schema)
    if mismatches != set():
        print("Data schema mismatch in message df!")
        print(mismatches)
        raise ValueError()

    # Reformat sent date
    message_df['sent_date'] = pd.to_datetime(message_df['sent_date'])

    # Set the heirarchical index
    new_index_tups = [(match_id, msg_num) for msg_num in message_df.index.values]
    new_index = pd.MultiIndex.from_tuples(new_index_tups, names = ["match_id", "msg_number"])
    message_df.index = new_index

    # Make new columns about message
    message_df["n_words_in_msg"]=message_df.apply(lambda x: len(x['message'].split(" ")), axis = 1)


    # New column about time of messages
    message_df['time_since_last_msg'] = message_df['sent_date'].diff()
    message_df['time_since_last_2_msgs'] = message_df['sent_date'].diff(2)
    # Think about escalation in message sending or if time between texts is small then...

    # Check for key words
    funny_words = ["hahaha", "lol", "haha", "ha"]
    message_df['funny_word_in_msg'] = message_df.apply(lambda x: word_list_in_phrase(funny_words, x['message']), axis =1 )

    question_words = ["?", "who", "what", "where", "when", "why", "how", "how's", "what's"]
    message_df['question_word_in_msg'] = message_df.apply(lambda x: word_list_in_phrase(question_words, x['message']), axis =1 )

    message_df['question_word_in_msg'] = message_df.apply(lambda x: 1 if "?" in x['message'] else x['question_word_in_msg'], axis = 1)

    return(message_df)
