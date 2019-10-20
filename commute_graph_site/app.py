import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/rwedell/data/master/commute_data_stacked_v2.csv')

app = dash.Dash()
server = app.server

app.title = "Commuter Graph"

#creating a dictionary of values for the state dropdown
state_options = []
for state in df['State'].unique():
    state_options.append({'label':str(state),'value':state})

markdown_text ="""
# Thanks for stopping by.
Use the dropdown, or better yet just start typing your favorite state in the box to find out how commuters get to work in different states.

This visual is built using Plotly and Dash and written in Python. Here's the [code](https://github.com/rwedell/commute_graph).

Follow this [link](https://rwedell.github.io/medianIncomeMap/) to see a map I made using JavaScript and Leflet. Here's the [repo](https://github.com/rwedell/rwedell.github.io/tree/master/medianIncomeMap).
"""

app.layout = html.Div([
    dcc.Markdown(children = markdown_text),
    html.Div([
        dcc.Dropdown(id = 'state-picker', 
                     options = state_options,
                     value='New York',
                     style = {'width':'50%'}),
        dcc.Graph(id='graph')        
    ])
    
    
])

@app.callback(Output('graph', 'figure'),
              [Input('state-picker', 'value')])
def update_figure(selected_state):
    filtered_df = df[df['State'] == selected_state]
    trace = []
    trace.append(go.Bar(
        x = filtered_df['Commute Type'],
        y = filtered_df['Rate']
        )
    )
    return {'data': trace,
            'layout':go.Layout(
                xaxis = {'title': selected_state},
                yaxis = {'title': "Percent of Commuters", 'showgrid':False},
                hovermode = "closest",
                title = "Commute Method by Percent in " + selected_state
                )
           }

if __name__ == '__main__':
    app.run_server()
