#----------------------------------------------------------------------------------------
#                      SOME NOTES ON DEVELOPMENT IDEAS / REQUIREMENTS
#---------------------------------------------------------------------------------------------
#
# AUTOMATICALLY SET TO MAXIMUM VALUE WHEN SUCH A DATASET IS CHOSEN AS ULTIMATE RATES ARE LIKELY TO BE RATES OF MOST INTEREST
# AND IT MAY GO UNOTICED BY USER THAT THEY ARE LOOKING AT SELECT RATES OTHERWISE.
#
# REMOVE ULTIMATE AGE MORTALITY RATES BECAUSE THEY DON'T LOOK NEAT ON THE GRAPH
# HOWEVER BE CARFUL OF WOL ASSURANCES IF USED WILL REQUIRE THEM 

# ADD IN LIFE OFFICE FUNCTIONS
#       A COUPLE OF KEY BADGES E.G. ASSURANCE FUNCTION; ANNUITY FUNCTION
#           FOR THE 3 (OR 2 OR 1) DATASETS CHOSEN THAT GIVES AN IDEA OF THE
#           FINANCIAL SIGNIFICANCE
#        WOULD BE NICE TO CALL ON ONE OF THE OPEN SOURCE ACTUARIAL LIBRARIES
#       IN ORDER TO DO THIS.
#           ANY LIMITING AGE WILL HAVE TO BE THE MINIMUM MAXIMUM AGE IN EACH DATASET
#           I THINK DATASETS THAT STOP AT SAY... BEFORE 90 SHOULD BE PREVENTED FROM
#           ANNUITIES BEING CALCULATED
# 
# MODIFY SLIDERS 
#           SO THAT DISPLAY ONLY WHEN APPROPRIATE DATASOURCE / TABLE DESCRIPTION CHOSEN
#           SO THAT THE YEAR SLIDER HAS INCREMENTS OF ONE YEAR AND 
#
#  GENERALLY SPEAKING THE UPDATE FIGURE CALLBACK COULD PROBABLY BENEFIT FROM HAVING MORE 
#  OF IT FUNCTION ' ISED
#
# MODIFY CALLBACKS SO THAT WHEN DATASOURCE CHANGES / TABLE DESCRIPTION AND PERHAPS ANY SLIDERS ARE CLEARED
#
#
# ADD IN DATASHEET THAT GIVES VISIBILITY OF THE UNDERLYING DATAFRAME
#                       https://dash.plotly.com/datatable
#
#
#
# DISPLAY OPTION TOGGLES    https://dash.plotly.com/dash-daq/toggleswitch
#       OPTION TOGGLE FOR DATASHEET VIEW
#       OPTION TOGGLE FOR LIFE OFFICE FUNCTION HIGHLIGHTS
#       OPTION TOGGLE FOR 
#
#
#  ADD IN COUNTRY FOR HMD
#  ADD IN MORE INFORMATION INTO THE LEGEND DESCRIPTION
#  GET LEGEND DESCRIPTION TO BE MORE INFORMATIVE
#
#
#  WOULD BE GOOD TO HAVE SOME DETAILED DESCRIPTIONS OF THE DATASETS AND LINKS TO THE SOURCE
#  DATA.




#----------------------------------------------------------------------------------------
#                      DEPENDENCIES
#---------------------------------------------------------------------------------------------
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
from datetime import datetime
import numpy as np
from functions.annuities.Repeatedly_Calling_AF import annuity_series

#----------------------------------------------------------------------------------------
#                      LOAD IN THE DATA
#---------------------------------------------------------------------------------------------

#OVERACHING TABLES
#-------------------------------------------------
# Load the summary table data
df_table_summary = pd.read_excel('Mortality_tables/Table_Summary.xlsx')


#IFOA TABLES
#---------------------------
# Open the '00 series file
#create a pandas/dataframe object
xlsx = pd.ExcelFile('Mortality_tables/00series.xls')
# Get the names of all the worksheets
worksheets = xlsx.sheet_names
#create empty dictionary to put all the worksheet names into
dfs = {}
# Read each worksheet into a dataframe and append it to the dictionary
for worksheet in worksheets:
    df = xlsx.parse(worksheet)
    dfs[worksheet] = df
#tables for 00series
#create empty list
series00_tables = []
#populate list with the names of '00 series tables
for i, option in enumerate(worksheets):
    series00_tables.append({'label': option, 'value': i+1})

# Open the '92 series file
#create a pandas/dataframe object
xlsx = pd.ExcelFile('Mortality_tables/92series.xls')
# Get the names of all the worksheets
worksheets = xlsx.sheet_names
#create empty dictionary to put all the worksheet names into
dfs = {}
# Read each worksheet into a dataframe and append it to the dictionary
for worksheet in worksheets:
    df = xlsx.parse(worksheet)
    dfs[worksheet] = df
#tables for 92series
#create empty list
series92_tables = []
#populate list with the names of '92 series tables
for i, option in enumerate(worksheets):
    series92_tables.append({'label': option, 'value': i+1})



#HUMAN MORTALITY DATABASE TABLES
#tables for HMD
HMD_table_1 = pd.read_csv('Mortality_tables/HMD_UK_males_1x1.txt')
HMD_table_2 = pd.read_csv('Mortality_tables/HMD_UK_females_1x1.txt')
HMD_table_3 = pd.read_csv('Mortality_tables/HMD_UK_both_sexes_1x1.txt')
HMD_tables = [HMD_table_1,HMD_table_2,HMD_table_3]
print(HMD_table_3.head)


#------------------------------------------------------------------------------------
#                   CREATE OPTIONS FOR DROPDOWNs
#------------------------------------------------------------------------------------

#overarching
#-------------------------------------------------------
#datasources dropdown
datasource_list = df_table_summary['Datasource'].unique().tolist()
datasource_list = sorted(datasource_list)
dsource_dropdown_options = []
for i, option in enumerate(datasource_list):
    dsource_dropdown_options.append({'label': option, 'value': i+1})


#initialising options for various dropdowns
options_dd_1 = []
options_dd_2 = []
options_dd_3 = []
options_td_1 = []
options_td_2 = []
options_td_3 = []


#IFOA TABLES
#---------------------------
#tables for 00series
#WE MAY BE ABLE TO GET RID OF THIS AS CREATING FUNCTION TO PROVIDE DESCRIPTION LIST
df_filtered = df_table_summary[df_table_summary['Datasource'] == 'IfoA 00 Series']
table_descriptions = df_filtered['Table Description'].tolist()



#----------------------------------------------------------------------------------------
#                          FUNCTIONS
#----------------------------------------------------------------------------------------

#functions that use the dataframe df_table_summary that was initialised from excel spreadsheet at start of script

def get_table_name_from_description(table_description):
    #print("get_table_name_from_description function called")
    result = df_table_summary.loc[df_table_summary['Table Description'] == table_description,'Table']
    return result.values.tolist()

def get_select_years_from_description(table_description):
    print("get_table_name_from_description function called")
    result = df_table_summary.loc[df_table_summary['Table Description'] == table_description,'Select Years']
    return result.values.tolist()

def get_datasource_location_from_description(table_description):
    #print("read_datasource_location function called")
    result = df_table_summary.loc[df_table_summary['Table Description'] == table_description,'Datasource Location']
    return result.values.tolist()

def get_datasource_from_description(table_description):
    #print("get_datasource_from_description function called")
    result = df_table_summary.loc[df_table_summary['Table Description'] == table_description,'Datasource']
    return result.values.tolist()

def get_table_description_list_from_datasource(dsource):
    print("get_table_description_list_from_datasource called")
    result = df_table_summary.loc[df_table_summary['Datasource'] == dsource,'Table Description']
    print("dsource fed into function is")
    print(dsource)
    print("head of the filtered dataframe is")
    print(result.head)
    return result.values.tolist()

#functions that work with the chosen dataframe for the figure

def get_dataframe_from_description(table_description):
    print("get_dataframe_from_description function called with:"+ str(table_description))
    #the means of obtaining a dataset is dependent on the dataset we are looking at
    #   for the 00 series there is a separate sheet for each table
    #   for the HMD......    
    if get_datasource_from_description(table_description) == ['IfoA 00 Series']:
        return pd.read_excel(get_datasource_location_from_description(table_description)[0], sheet_name=get_table_name_from_description(table_description)[0])
    elif get_datasource_from_description(table_description) == ['Human Mortality Database']:
        print(pd.read_csv((get_datasource_location_from_description(table_description)[0]),header=1,delim_whitespace=True).head)
        return pd.read_csv(get_datasource_location_from_description(table_description)[0],header=1,delim_whitespace=True)
    elif get_datasource_from_description(table_description) == ['IfoA 92 Series']:
        return pd.read_excel(get_datasource_location_from_description(table_description)[0], sheet_name=get_table_name_from_description(table_description)[0])
    else:
        print("get_dataframe_from_description function aint returning proper when the following table description passed thru: "+ str(table_description))
        return [0]
    

def get_x_axis_values_from_chosen_dataset(dset,table_description,year_slider):
    print("get_x_axis_values_from_chosen_dataset function called")
    if get_datasource_from_description(table_description) == ['IfoA 00 Series']:
        print("returning 00 series")
        return dset['Age x']
    elif get_datasource_from_description(table_description) == ['Human Mortality Database']:
        return dset.loc[dset['Year'] == year_slider,'Age']
        #return dset['Age']['Year'==year_slider]
    elif get_datasource_from_description(table_description) == ['IfoA 92 Series']:
        return dset['Age x']
    else:
        print("get_x_axis_values_from_chosen_dataset function aint returning proper")
        return [0]*30

def get_y_axis_values_from_chosen_dataset(dset,table_description,duration,year_slider):
    print("get_x_axis_values_from_chosen_dataset function called")
    if get_datasource_from_description(table_description) == ['IfoA 00 Series']:
        return dset[duration]
    elif get_datasource_from_description(table_description) == ['Human Mortality Database']:
        return dset.loc[dset['Year'] == year_slider,'qx']
        #return dset['qx']['Year'==year_slider]
    elif get_datasource_from_description(table_description) == ['IfoA 92 Series']:
        return dset[duration]
    else:
        print("get_x_axis_values_from_chosen_dataset function aint returning proper")
        return [0]*30

#-----------------------------------------------------------------------------------
#                       OBJECTS FOR GRAPH
#---------------------------------------------------------------------------------

# THIS SECTION SEEMS LIKE A BIT OF A FRUITLESS EXECISE
# WE POPULATE SOME DATASETS FOR THE GRAPH
# JUST SO THAT WE DON'T GET AN ERROR WHERE THE PAGE FIRST TRIES TO CREATE A FIGURE
# WE MAY LOOK AT SOLUTIONS IN THE FUTURE TO REMOVE THIS SECTION IN ORDER TO MAKE THE CODE
# MORE SUCCINCT
df_dset_1  = pd.read_excel('Mortality_tables/00series.xls', sheet_name='AMC00')
trace_1 = go.Scatter(x=df_dset_1['Age x'], y=df_dset_1['Duration 0'])
df_dset_2  = pd.read_excel('Mortality_tables/00series.xls', sheet_name='AMS00')
trace_2 = go.Scatter(x=df_dset_2['Age x'], y=df_dset_2['Duration 0'])
df_dset_3  = pd.read_excel('Mortality_tables/00series.xls', sheet_name='AMN00')
trace_3 = go.Scatter(x=df_dset_3['Age x'], y=df_dset_3['Duration 0'])
fig = go.Figure(data=[trace_1, trace_2, trace_3])

#-------------------------------------------------------------------------------------
#                SORT THE APP AND THE SERVER
#--------------------------------------------------------------------------

# Initialize the app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

#-------------------------------------------------------------------------------------
#           CREATE SOME CARD OBJECTS
#-------------------------------------------------------------------------------------

blue_card = dbc.Card(
            [
                html.H4("Mortality Data Dashboard", className="card-title", style={'color': '#C3941E'}),
                html.P("Explore Open Source Datasets", className="card-text", style={'color': '#FFFFFF'}),
            ],
            body=True,
            style={'background-color': '#002C53'}
            )


dataset1_card = dbc.Card(
                        [
                            dbc.CardBody(
                                [
                                            html.B("Dataset 1"),
                                            html.Br(),
                                            html.Br(),
                                            dbc.Label("Datasource"),
                                            dcc.Dropdown(id='dsource_dropdown_1',options=dsource_dropdown_options,value=None,style={'font-size':'12px'}),
                                            html.Br(),
                                            dbc.Label("Description"),
                                            html.Br(),
                                            dcc.Dropdown(id='description_dropdown_1',options=options_dd_1,value=None,placeholder='Please Select',style={'font-size':'12px'}),                                            
                                            
                                            html.Br(),
                                            html.Div([
                                                dbc.Label("Number of Select Years (max = ultimate)"),
                                                dcc.Slider(id='select_slider_1',min=0, max=5, value=0,step=1, marks={i: str(i) for i in range(1,6)})
                                            ], style= {'display': 'none'},id='slider_block_1'),
                                            html.Div([
                                                dbc.Label("Year of Data Collection"),
                                                dcc.Slider(id='year_slider_1',min=1920, max=2020, value=2020,step=1,included=False,tooltip={"placement": "bottom", "always_visible": True}, marks={i: str(i) for i in range(1920,2021,10)})
                                            ], style= {'display': 'none'},id='year_block_1')
                                ]
                            )
                        ]

                        )

dataset2_card = dbc.Card(
                        [
                            dbc.CardBody(
                                [
                                            html.B("Dataset 2"),
                                            html.Br(),
                                            html.Br(),
                                            dbc.Label("Datasource"),
                                            dcc.Dropdown(id='dsource_dropdown_2',options=dsource_dropdown_options,value=None,style={'font-size':'12px'}),
                                            html.Br(),
                                            dbc.Label("Description"),
                                            html.Br(),
                                            dcc.Dropdown(id='description_dropdown_2',options=options_dd_2,value=None,placeholder='Please Select',style={'font-size':'12px'}),                                            
                                            
                                            html.Br(),
                                            html.Div([
                                                dbc.Label("Number of Select Years (max = ultimate)"),
                                                dcc.Slider(id='select_slider_2',min=0, max=5, value=0,step=1, marks={i: str(i) for i in range(6)})
                                            ], style= {'display': 'none'},id='slider_block_2'),
                                            html.Div([
                                                dbc.Label("Year of Data Collection"),
                                                dcc.Slider(id='year_slider_2',min=1920, max=2020, value=2020,step=1,included=False,tooltip={"placement": "bottom", "always_visible": True}, marks={i: str(i) for i in range(1920,2021,10)})
                                            ], style= {'display': 'none'},id='year_block_2')
                                ]
                            )
                        ]

                        )

dataset3_card = dbc.Card(
                        [
                            dbc.CardBody(
                                [
                                            html.B("Dataset 3"),
                                            html.Br(),
                                            html.Br(),
                                            dbc.Label("Datasource"),
                                            dcc.Dropdown(id='dsource_dropdown_3',options=dsource_dropdown_options,value=None,style={'font-size':'12px'}),
                                            html.Br(),
                                            dbc.Label("Description"),
                                            html.Br(),
                                            dcc.Dropdown(id='description_dropdown_3',options=options_dd_1,value=None,placeholder='Please Select',style={'font-size':'12px'}),                                            
                                            
                                            html.Br(),
                                            html.Div([
                                                dbc.Label("Number of Select Years (max = ultimate)"),
                                                dcc.Slider(id='select_slider_3',min=0, max=5, value=0,step=1, marks={i: str(i) for i in range(6)})
                                            ], style= {'display': 'none'},id='slider_block_3'), 
                                            html.Div([
                                                dbc.Label("Year of Data Collection"),
                                                dcc.Slider(id='year_slider_3',min=1920, max=2020, value=2020,step=1,included=False,tooltip={"placement": "bottom", "always_visible": True}, marks={i: str(i) for i in range(1920,2021,10)})
                                            ], style= {'display': 'none'},id='year_block_3')                                               
                                ]
                            )
                        ]

                        )

type_of_graph_card = dbc.Card(
    [
        dbc.Row(
            [
                dbc.Col(html.B("Chart Type"), width=2,style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}),
                dbc.Col(dcc.Dropdown(id='chart_type_dropdown', placeholder='line',options=[{'label': 'Line', 'value': 'line'}, {'label': 'Bar', 'value': 'bar'}], value='line'), width=10)
            ]
        )
    ]
)

 


output_card = dbc.Card(
            [
                
                dcc.Graph(figure=fig,id='graph'),
                dbc.Label("Truncate X-Axis"),
                dcc.RangeSlider(0,120,10,value=[0,120],
                    id='graph_slider',allowCross=False,pushable=20),
                dbc.Label("Truncate Y-Axis"),
                dcc.RangeSlider(0,1,0.1,value=[0,1],
                    id='graph_slider2',allowCross=False,pushable=0.1
                )
            ]
        )
output_card2 = dbc.Card(
            [
                
                dcc.Graph(figure=fig,id='graph2'),
                dbc.Label("Truncate X-Axis"),
                #dcc.RangeSlider(0,120,10,value=[0,120],
                #    id='graph_slider',allowCross=False,pushable=20),
                #dbc.Label("Truncate Y-Axis"),
                #dcc.RangeSlider(0,1,0.1,value=[0,1],
                #    id='graph_slider2',allowCross=False,pushable=0.1
                #)
            ]
        )


Disclaimer_card =  dbc.Card(
            [
                html.Div("Disclaimer: This webapp has been prepared by the Institute and Faculty of Actuaries (IFoA). The IFoA does not accept any responsibility and/or liability whatsoever for the content or use of this webapp. This webapp does not constitute advice and should not be relied upon as such. The IFoA does not guarantee any outcome or result from the application of this webapp and no warranty as to the accuracy or correctness of this webapp is provided."),
                html.Br(),
                html.Div("Copyright: All material in this webapp is the copyright material of the IFoA, unless otherwise stated. Use may be made of this webapp for non-commercial and study/research purposes without permission from the IFoA. Commercial use of this webapp may only be made with the express, prior written permission of the IFoA.")
            ]
        )

#------------------------------------------------------------------------------------
#                              CALLBACK FUNCTIONS
#------------------------------------------------------------------------------------
# we have 4 callback functions.  3 of them relate to changes that occur when the datasource is updated and also the table description are updated.  the inputs are these 2 aforementioned items.  
# If HMD datasource is selected we display the year_block year sliders.
# other outputs options for the description and table dropdowns... which naturally result from the choice of datasource

# the other callback function is to update the figure....  however it is doing a whole lot more than just this
# it registers a change in the table name, a change in chart type, a change in the value on the select slider
# a change on any of the chart sliders for truncating axes
# 
# a thing that is proving tricky to implement is to get rid of the 3rd input... the table name itself 
# as would be a more user friendly interface with only the table description



@app.callback(
    [dash.dependencies.Output('description_dropdown_1', 'options'),Output(component_id='year_block_1', component_property='style')],
    [dash.dependencies.Input('dsource_dropdown_1', 'value'),dash.dependencies.Input('description_dropdown_1', 'value')]
)
def update_table1_options_from_dsource(dsource,descrip):
    print("def update_table1_options_from_dsource has been called {}".format(datetime.now()))
    if dsource_dropdown_options[dsource-1]['label'] == 'IfoA 00 Series':
        return get_table_description_list_from_datasource(dsource_dropdown_options[dsource-1]['label']),{'display': 'none'}
    elif dsource_dropdown_options[dsource-1]['label'] == 'Human Mortality Database':
        return get_table_description_list_from_datasource(dsource_dropdown_options[dsource-1]['label']),{'display': 'block'}
    elif dsource_dropdown_options[dsource-1]['label'] == 'IfoA 92 Series':
        return get_table_description_list_from_datasource(dsource_dropdown_options[dsource-1]['label']),{'display': 'none'}
    else:
        year_block_1 = {'display': 'none'}
        return [{'label': 'ONS tables to be added Q1 2023'},year_block_1]

@app.callback(
    [dash.dependencies.Output('description_dropdown_2', 'options'),Output(component_id='year_block_2', component_property='style')],
    [dash.dependencies.Input('dsource_dropdown_2', 'value'),dash.dependencies.Input('description_dropdown_2', 'value')]
)
def update_table2_options_from_dsource(dsource,descrip):
    print("def update_table2_options_from_dsource has been called at {}".format(datetime.now()))  
    if dsource_dropdown_options[dsource-1]['label'] == 'IfoA 00 Series':
        return get_table_description_list_from_datasource(dsource_dropdown_options[dsource-1]['label']),{'display': 'none'}
    elif dsource_dropdown_options[dsource-1]['label'] == 'Human Mortality Database':
        return get_table_description_list_from_datasource(dsource_dropdown_options[dsource-1]['label']),{'display': 'block'}
    elif dsource_dropdown_options[dsource-1]['label'] == 'IfoA 92 Series':
        return get_table_description_list_from_datasource(dsource_dropdown_options[dsource-1]['label']),{'display': 'none'}
    else:
        year_block_2 = {'display': 'none'}
        return [{'label': 'ONS tables to be added Q1 2023'},year_block_2]


@app.callback(
    [dash.dependencies.Output('description_dropdown_3', 'options'),Output(component_id='year_block_3', component_property='style')],
    [dash.dependencies.Input('dsource_dropdown_3', 'value'),dash.dependencies.Input('description_dropdown_3', 'value')]
)
def update_table3_options_from_dsource(dsource,descrip):
    print("def update_table3_options_from_dsource has been called at {}".format(datetime.now()))
    if dsource_dropdown_options[dsource-1]['label'] == 'IfoA 00 Series':
        return get_table_description_list_from_datasource(dsource_dropdown_options[dsource-1]['label']),{'display': 'none'}
    elif dsource_dropdown_options[dsource-1]['label'] == 'Human Mortality Database':
        return get_table_description_list_from_datasource(dsource_dropdown_options[dsource-1]['label']),{'display': 'block'}
    elif dsource_dropdown_options[dsource-1]['label'] == 'IfoA 00 Series':
        return get_table_description_list_from_datasource(dsource_dropdown_options[dsource-1]['label']),{'display': 'none'}
    else:
        year_block_3 = {'display': 'none'}
        return [{'label': 'ONS tables to be added Q1 2023'},year_block_3]


@app.callback(
    [Output(component_id='graph', component_property='figure'),Output(component_id='select_slider_1', component_property='max'),Output(component_id='select_slider_2', component_property='max'),Output(component_id='select_slider_3', component_property='max'),Output(component_id='slider_block_1', component_property='style'),Output(component_id='slider_block_2', component_property='style'),Output(component_id='slider_block_3', component_property='style')],
    [Input(component_id='chart_type_dropdown', component_property='value'),
     Input(component_id='select_slider_1', component_property='value'),
     Input(component_id='select_slider_2', component_property='value'),
     Input(component_id='select_slider_3', component_property='value'),
     Input(component_id='graph_slider', component_property='value'),
     Input(component_id='graph_slider2', component_property='value'),
     dash.dependencies.Input('description_dropdown_1', 'value'),
     dash.dependencies.Input('description_dropdown_2', 'value'),
     dash.dependencies.Input('description_dropdown_3', 'value'),
     dash.dependencies.Input('year_slider_1', 'value'),
     dash.dependencies.Input('year_slider_2', 'value'),
     dash.dependencies.Input('year_slider_3', 'value')]
)
def update_figure(chart_type,slider_1,slider_2,slider_3,graph_slider_value,graph_slider_value2,descrip1,descrip2,descrip3,year_slider_1,year_slider_2,year_slider_3):
    print("def update_figure has been called at {}".format(datetime.now()))


    #OBTAIN THE DATASET THAT IS DEPENDENT ON
    #THE DATA DESCRIPTION THAT HAS BEEN CHOSEN.
    df_dset_1 = get_dataframe_from_description(descrip1)
    df_dset_2 = get_dataframe_from_description(descrip2)
    df_dset_3 = get_dataframe_from_description(descrip3)

    data = []

    #USE SLIDER VALUES TO DETERMINE LOOKUP FIELD VALUE
    #THIS IS ALSO VERY SPECIFIC TO THE 00 SERIES FIELD NAMES
    #AND WOULD PROBABLY BE BEST TAKEN OUT INTO A FUNCTION
    #AND THE CALLBACK FUNCTION MADE MORE GENERALISED FOR ALL DATASETS
    duration_dset_1 = "Duration "+ str(slider_1)
    duration_dset_2 = "Duration "+ str(slider_2)    
    duration_dset_3 = "Duration "+ str(slider_3)
    print("         duration dset 1 is:"+str(duration_dset_1)+";"+"duration dset 2 is:"+str(duration_dset_2)+";"+"duration dset 3 is:"+str(duration_dset_3))

    #determine max select years for each table description choice
    max_select_dset_1 = get_select_years_from_description(descrip1)
    max_select_dset_2 = get_select_years_from_description(descrip2)
    max_select_dset_3 = get_select_years_from_description(descrip3)
    #and consequently determine which slider blocks to display
    if max_select_dset_1 == [0]:
        slider_block_1 = {'display': 'none'}
    else:
        slider_block_1 = {'display': 'block'}
    if max_select_dset_2 == [0]:
        slider_block_2 = {'display': 'none'}
    else:
        slider_block_2 = {'display': 'block'}
    if max_select_dset_3 == [0]:
        slider_block_3 = {'display': 'none'}
    else:
        slider_block_3 = {'display': 'block'}


    print("     graph slider value is:"+str(graph_slider_value))
       

# we have a dataframe df_dset_1 2 and 3
# OUR TRACE VARIABLES HOLD A BIT MORE INFO ON TYPE OF GRAPH AND CHOOSE APPROPRIATE COLUMS FROM OUR DATAFRAMES
# IN ORDER SET X AND Y AXIS
    if get_table_name_from_description(descrip1) is not None:
        if chart_type == 'line':
            trace_1 = go.Scatter(x=get_x_axis_values_from_chosen_dataset(df_dset_1,descrip1,year_slider_1), y=get_y_axis_values_from_chosen_dataset(df_dset_1,descrip1,duration_dset_1,year_slider_1), name=str(get_table_name_from_description(descrip1)), marker=dict(color="#abe2fb"))
        elif chart_type == 'bar':
            trace_1 = go.Bar(x=get_x_axis_values_from_chosen_dataset(df_dset_1,descrip1,year_slider_1), y=get_y_axis_values_from_chosen_dataset(df_dset_1,descrip1,duration_dset_1,year_slider_1), name=str(get_table_name_from_description(descrip1)), marker=dict(color="#abe2fb"))
        data.append(trace_1)
    #removing bar if nothing selected



    if get_table_name_from_description(descrip2) is not None:
        if chart_type == 'line':
            trace_2 = go.Scatter(x=get_x_axis_values_from_chosen_dataset(df_dset_2,descrip2,year_slider_2), y=get_y_axis_values_from_chosen_dataset(df_dset_2,descrip2,duration_dset_2,year_slider_2), name=str(get_table_name_from_description(descrip2)),marker=dict(color="#002c53"))
        elif chart_type == 'bar':
            trace_2 = go.Bar(x=get_x_axis_values_from_chosen_dataset(df_dset_2,descrip2,year_slider_2), y=get_y_axis_values_from_chosen_dataset(df_dset_2,descrip2,duration_dset_2,year_slider_2), name=str(get_table_name_from_description(descrip2)),marker=dict(color="#002c53"))
        data.append(trace_2)

    if get_table_name_from_description(descrip3) is not None:
        if chart_type == 'line':
            trace_3 = go.Scatter(x=get_x_axis_values_from_chosen_dataset(df_dset_3,descrip3,year_slider_3), y=get_y_axis_values_from_chosen_dataset(df_dset_3,descrip3,duration_dset_3,year_slider_3),name=str(get_table_name_from_description(descrip3)),marker=dict(color=" #c3941e"))
        elif chart_type == 'bar':
            trace_3 = go.Bar(x=get_x_axis_values_from_chosen_dataset(df_dset_3,descrip3,year_slider_3), y=get_y_axis_values_from_chosen_dataset(df_dset_3,descrip3,duration_dset_3,year_slider_3), name=str(get_table_name_from_description(descrip3)),marker=dict(color=" #c3941e"))
        data.append(trace_3)

    #ensuring that no graph lines are shown on initial load
    if descrip1 == None and descrip2 == None and descrip3 == None :
        print("called")
        data=[]
    

    fig = go.Figure(data=data)

    y_max_list =[]
    # iterate through the traces
    for trace in fig.data:
        # find the maximum y value for the current trace
        y_max = max(trace.y)
        # append the maximum y value to the list
        y_max_list.append(y_max)




    # Set the xaxis title to "Age"
    fig.update_layout(xaxis=dict(title="Ageₓ"))
    # Set the yaxis title to "qₓ"
    fig.update_layout(yaxis=dict(title="qₓ"))
    fig.update_layout(
                    paper_bgcolor='white',
                    plot_bgcolor='white',
                    xaxis=dict(gridcolor='white',range=graph_slider_value))
    
    fig.update_layout(yaxis=dict(gridcolor='white', range=graph_slider_value2))


    #we don't want to calculate any annuity functions unless maximum select period is chosen.
    #we therefore need a function to check maximum select period
    #or determine not relevant
    #we would also benefit from the figure being in a different tab and a different callback function because
    #where it is currently located significantly slows down processing.

    print (df_dset_1.head)
    #newdf to feed into function
    s1 = get_x_axis_values_from_chosen_dataset(df_dset_1,descrip1,year_slider_1)
    s2 = get_y_axis_values_from_chosen_dataset(df_dset_1,descrip1,duration_dset_1,year_slider_1)
    df = pd.concat([s1, s2], axis=1)
    print("column titles")
    df = df.rename(columns={df.columns[1]: "Rates"})
    print(df.columns)
    print("the df we are feeding in is:")
    print(df)


    annuity_series(df,0.04)


    #return fig,max_select_dset_1,max_select_dset_2,max_select_dset_3,slider_block_1,slider_block_2,slider_block_3

    return (fig,
            max_select_dset_1,
            max_select_dset_2,
            max_select_dset_3,
            slider_block_1,
            slider_block_2,
            slider_block_3)


# --------------------------------------------------------------------------------------
#                   SET THE LAYOUT OF THE APP
#---------------------------------------------------------------------------------------

fred = html.Div([dataset1_card, dataset2_card, dataset3_card],style={'overflow-y': 'scroll', 'height': '50%'})

# Calculate the height of blue_card in pixels
blue_card_height = 10  # Replace with the actual height of blue_card
offset_value = str(blue_card_height) + "px"

column1 = dbc.Col([blue_card,fred ],width=4,style={'background-color': '#F3F5F7'})
    

column2 = dbc.Col(
    [html.Div(style={"height": offset_value}), type_of_graph_card,html.Div(style={"height": offset_value}),output_card,html.Div(style={"height": offset_value}),output_card2,html.Div(style={"height": offset_value}),Disclaimer_card],
    width=8,
    style={'background-color': '#F3F5F7'}
)

app.layout = html.Div(
    [        dbc.Row([column1, column2]),
    ]
)



#---------------------------------------------------------------------------------------
# Run the app
if __name__ == '__main__':
    app.run_server()







