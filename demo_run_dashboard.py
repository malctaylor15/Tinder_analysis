
# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import json
from Scripts import message_df_fx as msg_fx

# Open and parse file
data_path = "Data/data.json"
with open(data_path, "rb") as inp:
    data = json.load(inp)
list_of_dfs = [msg_fx.get_msg_df(msg_dict) for msg_dict in data["Messages"]]
all_msg_df = pd.concat(list_of_dfs, axis=0)
all_msg_df['date'] = all_msg_df['sent_date'].dt.date

date_gb = all_msg_df[['n_words_in_msg', 'date']].groupby('date')
date_agg = date_gb.count()

trace = go.Scatter(
    x=date_agg.index,
    y=date_agg['n_words_in_msg'],
    mode='lines',
    name='Number of Words in Message'
    )


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='Hello Dash',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    html.Div(children='Dash: A web application framework for Python.', style={
        'textAlign': 'center',
        'color': colors['text']
    }),

    dcc.Graph(
        id='example-graph-2',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
            ],
            'layout': {
                'plot_bgcolor': colors['background'],
                'paper_bgcolor': colors['background'],
                'font': {
                    'color': colors['text']
                }
            }
        }
    )
])






if __name__ == '__main__':
    app.run_server(debug=True)