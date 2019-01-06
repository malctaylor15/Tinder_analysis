## This script has most of the functions for analyzing the usage

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import re

from Scripts import EDA_functions as mt_eda

def gather_usage_stats(usage_df):

    usage_sums = usage_df.sum()
    derived_metrics = {}
    # Number of swipes
    derived_metrics["total_swipes"] = usage_sums['swipes_likes'] + usage_sums['swipes_passes']
    # Likes to passes (for every 1 pass there are x likes )
    derived_metrics["like_to_pass_ratio"] = usage_sums['swipes_likes']/usage_sums['swipes_passes']
    # Number of swipes per app open
    derived_metrics["swipes/app_open"] = (usage_sums['swipes_likes'] + usage_sums['swipes_passes']) / usage_sums[
        'app_opens']
    # Avg Messages recieved per match
    derived_metrics["n_avg_msg_rec_per_match"] = usage_sums['messages_received'] / usage_sums['matches']
    # Avg Messages sent per match
    derived_metrics["n_avg_msg_sent_per_match"] = usage_sums['messages_sent'] / usage_sums['matches']
    # Calendar days on tinder
    days_on_tinder = pd.to_datetime(usage_df.iloc[-1].name) - pd.to_datetime(usage_df.iloc[0].name)
    days_on_tinder = days_on_tinder.days
    # Days when you opened the app
    active_days_on_tinder = len(usage_df.index)

    # Avg Swipes per day
    derived_metrics["swipes_per_tot_cal_day"] = derived_metrics["total_swipes"] / days_on_tinder
    derived_metrics["swipes_per_act_day"] = derived_metrics["total_swipes"] / active_days_on_tinder

    derived_metrics = {k: np.round(v, 2) for k, v in derived_metrics.items()}

    return(derived_metrics)

def gather_max_usage(usage_df):

    # Dates of max_usage
    max_usage = pd.concat([usage_df.idxmax(), usage_df.max()], keys=["date", "max of index"], axis = 1)
    return(max_usage)


def get_usage_time_series_plots(agg_series):
    """
    Plot several metrics for time series data

    agg_series (dict):
        key: string of which aggregation is used
        value: (pd.Series) Time series of metric with the index being a string of the year+month

    fig: (matplotlib figure) Returns plot with each aggregated metric in a row
    """
    n_sub_plots = len(agg_series)
    fig = plt.figure()
    plot_index = 0

    for name, series in agg_series.items():
        plot_index = plot_index + 1
        ax = fig.add_subplot(n_sub_plots, 1, plot_index)
        ax.plot(series)
        ax.set_title("Monthly " + name + " (per day)")
        ax.grid(True)
        # Show every n (3rd) label on x axis
        n = 3
        for index, label in enumerate(ax.xaxis.get_ticklabels()):
            if index % n != 0:
                label.set_visible(False)

        fig.autofmt_xdate()
        ax.set_xlabel("Year + Month")
        y_label_str = name.replace('mean', '')
        y_label_str = y_label_str.replace('max', '')
        ax.set_ylabel("Number of " + y_label_str)
    fig.tight_layout()

    return (fig)


def plot_table(text_df, text=""):
    """
    Plot pandas df as table in matplotlib

    Input:
        text_df (pd.DataFrame): table (values) will be plotted in matplotlib figure
        text (str): string that will be in upper left hand corner of plot image
    Returns:
        fig (matplotlib plt)

    """

    # Create figure
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.axis('off')
    ax.axis('tight')
    # Input data into plot
    ax.table(cellText=text_df.values
             , colLabels=text_df.columns
             , loc='center')

    ax.text(0.05, 0.95, text, transform=fig.transFigure, size=16)
    fig.tight_layout()

    return (fig)

def create_usage_plots(usage_df):

    # Generate some statistics
    max_usage = gather_max_usage(usage_df)
    derived_metrics = gather_usage_stats(usage_df)
    derived_metrics_df = pd.Series(derived_metrics).reset_index().rename({'index': "metric", 0: "value"}, axis=1)
    # Generate matplotlib plots from stats
    max_usg_tbl = plot_table(max_usage, text="Max Usage")
    derived_metrics_tbl = plot_table(derived_metrics_df, text="Derived Metrics")

    # Save plots
    plt_dict = {"max_usage_plt":max_usg_tbl , "derived_metrics_plt" : derived_metrics_tbl}

    # Begin creating aggregated time series plots
    usage_df2 = usage_df.copy()
    usage_df2.index = pd.to_datetime(usage_df.index, format="%Y-%m-%d")
    usage_df2.index = pd.Series(usage_df2.index).apply(mt_eda.flatten_date)

    # Create aggregated time series data and plots
    funcs = {"mean": np.mean, "max": np.max}  # , "std":np.std}
    for usage_col in usage_df2.columns:
        gb_dt = pd.Series(usage_df2[usage_col]).groupby(usage_df2.index)
        agg_series = {usage_col + " " + func_names: gb_dt.apply(func) for func_names, func in funcs.items()}
        plts = get_usage_time_series_plots(agg_series)
        plt_dict[usage_col] = plts

    return(plts)



