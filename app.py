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

#------------------------------------------------------------------------------------
#                   CREATE OPTIONS FOR DROPDOWNs
#------------------------------------------------------------------------------------

#tables for 00series
series00_tables = []
for i, option in enumerate(worksheets):
    series00_tables.append({'label': option, 'value': i+1})

#tables for 00series
df_filtered = df_table_summary[df_table_summary['Datasource'] == 'IfoA 00 Series']
table_descriptions = df_filtered['Table Description'].tolist()

#dropdown options for datasources
datasource_list = df_table_summary['Datasource'].unique().tolist()

dsource_dropdown_options = []
for i, option in enumerate(datasource_list):
    dsource_dropdown_options.append({'label': option, 'value': i+1})

print(dsource_dropdown_options)



#options for various dropdowns
options_dd_1 = []
options_dd_2 = []
options_dd_3 = []
options_td_1 = []
options_td_2 = []
options_td_3 = []
#-----------------------------------------------------------------------------------
#                       OBJECTS FOR GRAPH
#---------------------------------------------------------------------------------

'''
df_dset_1  = pd.read_excel('Mortality_tables/00series.xls', sheet_name='AMC00')
#fig = px.line(df_dset_1, x="Age x", y="Duration 0")
#fig = px.line()
trace_1 = go.Scatter(x=df_dset_1['Age x'], y=df_dset_1['Duration 0'])
# Add the trace to the plot
#fig.add_trace(trace)


df_dset_2  = pd.read_excel('Mortality_tables/00series.xls', sheet_name='AMS00')
# Create a trace object for df_dset_2 using the go.Scatter constructor
trace_2 = go.Scatter(x=df_dset_2['Age x'], y=df_dset_2['Duration 0'])
# Add the trace to the plot
#fig.add_trace(trace)

df_dset_3  = pd.read_excel('Mortality_tables/00series.xls', sheet_name='AMN00')
# Create a trace object for df_dset_2 using the go.Scatter constructor
trace_3 = go.Scatter(x=df_dset_3['Age x'], y=df_dset_3['Duration 0'])
# Add the trace to the plot
#fig.add_trace(trace)

fig = go.Figure(data=[trace_1, trace_2, trace_3])

'''



#-------------------------------------------------------------------------------------

#--------------------------------------------------------------------------

# Initialize the app
app = dash.Dash()
server = app.server



























#-------------------------------------------------------------------------------------

#--------------------------------------------------------------------------











#---------------------------------------

# Initialize the app


#Create a dropdown menu for selecting the chart type
chart_type_menu = dcc.Dropdown(
    id='chart-type-menu',
    options=[
        {'label': 'Line chart', 'value': 'line'},
        {'label': 'Bar chart', 'value': 'bar'}
    ],
    value='line'
)


# Create a Dash layout
app.layout = html.Div([
    chart_type_menu

])















# Run the app
if __name__ == '__main__':
    app.run_server()







