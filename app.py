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





























#-------------------------------------------------------------------------------------

#--------------------------------------------------------------------------











#---------------------------------------

# Import the MySQL connector
import mysql.connector
import pandas as pd

# Load the data
df = pd.read_excel('Mortality_tables/ams00.xls')

#print what has been retrieved
#print(df.head)

#-------------------------------------------------------------



# Initialize the app
app = dash.Dash()
server = app.server

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







