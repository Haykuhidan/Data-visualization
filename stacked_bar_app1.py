#!/usr/bin/env python
# coding: utf-8

# In[4]:


import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

data = pd.read_csv("data_cleaned.csv")


app = dash.Dash(__name__)


# In[5]:


data.head()


# In[8]:


type_options = data["NAME_CONTRACT_TYPE"].unique()


# In[9]:


app = dash.Dash()

app.layout = html.Div([
    html.H2("Credit amount report"),
    html.Div(
        [
            dcc.Dropdown(
                id="Type",
                options=[{
                    'label': i,
                    'value': i
                } for i in type_options],
                value='All Types'),
        ],
        style={'width': '25%',
               'display': 'inline-block'}),
    dcc.Graph(id='funnel-graph'),
])


# In[15]:


@app.callback(
    dash.dependencies.Output('funnel-graph', 'figure'),
    [dash.dependencies.Input('Type', 'value')])
def update_graph(Type):
    if Type == "All Types":
        df_plot = data.copy()
    else:
        df_plot = data[data['NAME_CONTRACT_TYPE'] == Type]

    pv = pd.pivot_table(
        df_plot,
        index=['NAME_FAMILY_STATUS'],
        columns=["NAME_EDUCATION_TYPE"],
        values=['AMT_CREDIT'],
        aggfunc=sum,
        fill_value=0)
    trace1 = go.Bar(x=pv.index, y=pv[('AMT_CREDIT', 'Academic degree')], name='credit academic degree')
    trace2 = go.Bar(x=pv.index, y=pv[('AMT_CREDIT', 'Higher education')], name='credit higher education')
    trace3 = go.Bar(x=pv.index, y=pv[('AMT_CREDIT', 'Incomplete higher')], name='credit Incomlete higher')
    trace4 = go.Bar(x=pv.index, y=pv[('AMT_CREDIT', 'Lower secondary')], name='credit Lower secondary')
    trace5 = go.Bar(x=pv.index, y=pv[('AMT_CREDIT', 'Secondary / secondary special')], name='credit Secondary')

    return {
    'data': [trace1, trace2, trace3, trace4,trace5],
    'layout':
    go.Layout(
        title='Credit amount of {}'.format(Type),
        barmode='stack')
}


# In[16]:


if __name__ == '__main__':
    app.run_server(debug=True)


# In[ ]:




