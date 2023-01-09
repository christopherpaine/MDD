#----------------------------------------------------------------------------------------
#                      LOAD IN THE DATA
#---------------------------------------------------------------------------------------------
#
import mysql.connector
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from dash.dependencies import Input, Output
import dash_daq as daq

import dash_bootstrap_components as dbc
import plotly.graph_objs as go


# Load the summary table data
df_table_summary = pd.read_excel('Mortality_tables/Table_Summary.xlsx')

# Open the Excel file
xlsx = pd.ExcelFile('Mortality_tables/00series.xls')
# Get the names of all the worksheets
worksheets = xlsx.sheet_names
#create empty dictionary to put all the worksheet names into
dfs = {}
# Read each worksheet into a dataframe and append it to the dictionary
for worksheet in worksheets:
    df = xlsx.parse(worksheet)
    dfs[worksheet] = df








#---------------------------------------

# Import the MySQL connector
import mysql.connector
import pandas as pd

# Load the data
df = pd.read_excel('Mortality_tables/ams00.xls')

#print what has been retrieved
#print(df.head)

#-------------------------------------------------------------
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from dash.dependencies import Input, Output
import dash_daq as daq
from layout_components import get_slider



# Initialize the app
app = dash.Dash()
server = app.server

# Create a plotly figure
fig = px.line(df, x='Age x', y='Duration 0')

#Create a dropdown menu for selecting the chart type
chart_type_menu = dcc.Dropdown(
    id='chart-type-menu',
    options=[
        {'label': 'Line chart', 'value': 'line'},
        {'label': 'Bar chart', 'value': 'bar'}
    ],
    value='line'
)

@app.callback(Output('chart', 'figure'),
              [Input('chart-type-menu', 'value')])
def update_chart(chart_type):
    if chart_type == 'line':
        fig = px.line(df, x='Age x', y='Duration 0')
    else:
        fig = px.bar(df, x='Age x', y='Duration 0')
    return fig

# callback to update the slider label
@app.callback(
    Output('output-1', 'children'),  # specify the output and the property to update
    [Input('slider-1', 'value')]  # specify the input
)
def update_output(value):
    return f'Age: {value}'




# Create a Dash layout
app.layout = html.Div([
    chart_type_menu,
    dcc.Graph(id='chart'),
        # Add a slider component
    dcc.Slider(
        id='slider',
        min=df['Age x'].min(),
        max=df['Age x'].max(),
        step=10,
        value=df['Age x'].min()
    ),
    # the slider
# Add a slider component
    get_slider(df),
    # the label
    html.Div(id='output-1')  # give the label an ID


])















# Run the app
if __name__ == '__main__':
    app.run_server()







