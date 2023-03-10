#----------------------------------------------------------------------------------------
#                      SOME NOTES ON DEVELOPMENT IDEAS / REQUIREMENTS
#---------------------------------------------------------------------------------------------
#
#
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
from scipy.interpolate import griddata
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
    result = df_table_summary.loc[df_table_summary['Table Description'] == table_description,'Table']
    if not result.empty:
        return result.values.tolist()
    else:
        return None

def get_select_years_from_description(table_description):
    #print("get_table_name_from_description function called")
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
    #print("get_dataframe_from_description function called with:"+ str(table_description))
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

#take in one or more arguments; return list of dataframes
def get_dataframe_from_description2(*table_descriptions):
    dataframes = []
    for table_description in table_descriptions:
        if get_datasource_from_description(table_description) == ['IfoA 00 Series']:
            dataframes.append(pd.read_excel(get_datasource_location_from_description(table_description)[0], sheet_name=get_table_name_from_description(table_description)[0]))
        elif get_datasource_from_description(table_description) == ['Human Mortality Database']:
            dataframes.append(pd.read_csv(get_datasource_location_from_description(table_description)[0],header=1,delim_whitespace=True))
        elif get_datasource_from_description(table_description) == ['IfoA 92 Series']:
            dataframes.append(pd.read_excel(get_datasource_location_from_description(table_description)[0], sheet_name=get_table_name_from_description(table_description)[0]))
        else:
            print("get_dataframe_from_description function aint returning proper when the following table description passed thru: "+ str(table_description))
            dataframes.append(pd.DataFrame())
    return dataframes




def get_x_axis_values_from_chosen_dataset(dset,table_description,year_slider):
    #print("get_x_axis_values_from_chosen_dataset function called")
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


def duration_headings_from_select_sliders(*slider_values):
    duration_titles=[]
    for slider_value in slider_values:
        duration_titles.append("Duration "+ str(slider_value))
    return duration_titles




#graph formatting functions

def set_figure_grid_white(fig):
    fig.update_layout(yaxis=dict(gridcolor='white'))
    fig.update_layout(xaxis=dict(gridcolor='white'))
    fig.update_layout(paper_bgcolor='white',plot_bgcolor='white', )
    return fig

def set_figure_axis_range(fig,x,y):
    fig.update_layout(yaxis=dict(range = y))
    fig.update_layout(xaxis=dict(range =x))

    return fig

def set_figure_titles(fig,x,y):
    fig.update_layout(xaxis=dict(title=x))
    fig.update_layout(yaxis=dict(title=y))
    return fig

def add_trace_to_figure_data(data,x_values,y_values,dropdown_description,colour,chart_type):
        if colour == 1:
            colr = "#abe2fb"
        elif colour == 2:
            colr = "#002c53"
        elif colour == 3:
            colr = "#c3941e"
        else:
            colr = "#000000" # default value
        trace = go.Scatter(x=x_values, y=y_values,name=str(get_table_name_from_description(dropdown_description)),marker=dict(color=colr))

        if chart_type == "line":
                    trace = go.Scatter(x=x_values, y=y_values,name=str(get_table_name_from_description(dropdown_description)),marker=dict(color=colr))
        elif chart_type == "bar":
                    trace = go.Bar(x=x_values, y=y_values,name=str(get_table_name_from_description(dropdown_description)),marker=dict(color=colr))
        data.append(trace)   
        #no need for return as passing in a mutable object   

def display_select_slider(descrip1,descrip2,descrip3):

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

    return  [max_select_dset_1,max_select_dset_2 ,max_select_dset_3 ,slider_block_1,slider_block_2,slider_block_3]







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
                
                dcc.Graph(
                    #figure=fig,
                    id='graph2'),
                    dbc.Label("Interest Rate"),


                        dcc.Slider(
                            id='int_rate_slider',
                            min=0.00,
                            max=0.20,
                            value=0.04,
                            step=0.01,
                            included=False,
                            tooltip={
                                "placement": "bottom",
                                "always_visible": True
                            },
                            marks={i: f"{i:.2f}" for i in np.arange(0.00, 0.20 + 0.01, 0.01)}
                        )
            ]
        )



#TEMPORARY CODE FOR A 3D GRAPH
d_data = get_dataframe_from_description2("HMD:  UK Males 1x1")
#d_data[0] is our dataframe because above function inconveniently returns a list
dfz = d_data[0]
x, y, z = (np.array(dfz[dfz['Age']!='110+'][col], dtype=float) for col in ['Age', 'Year', 'qx'])
xi, yi = np.linspace(x.min(), x.max(), 100), np.linspace(y.max(), y.min(), 100)
X, Y = np.meshgrid(xi, yi)
Z = griddata((x,y),z,(X,Y), method='cubic')
fig3D = go.Figure(go.Surface(x=xi,y=yi,z=Z,colorscale ='Blues'))

fig3D.update_layout(title='HMD:  UK Males 1x1', autosize=False,
                  width=500, height=500,scene=dict(
xaxis_title='Age',
yaxis_title='Year',
zaxis_title='q_x'
)
                  #margin=dict(l=65, r=50, b=65, t=90)
                  )

z = np.log(z)
Z = griddata((x,y),z,(X,Y), method='cubic')
fig3Dv2 = go.Figure(go.Surface(x=xi,y=yi,z=Z,colorscale ='Blues'))

fig3Dv2.update_layout(title='using log of mortality rate', autosize=False,
                  width=500, height=500,scene=dict(
xaxis_title='Age',
yaxis_title='Year',
zaxis_title='q_x'
)
                  #margin=dict(l=65, r=50, b=65, t=90)
                  )




'''
output_card3 = dbc.Card(
            [
                
                dcc.Graph(
                    figure=fig3D,
                    id='graph3')
                    ,
                     dcc.Graph(
                    figure=fig3Dv2,
                    id='graph4')
            ]
        )
'''
output_card3 = dbc.Card(
    [
        dbc.Row(
            [
                dbc.Col(dcc.Graph(figure=fig3D, id='graph3'), width=6),
                dbc.Col(dcc.Graph(figure=fig3Dv2, id='graph4'), width=6)
            ]
        )
    ]
)











Disclaimer_card =  dbc.Card(
            [
                html.Div("Disclaimer: This webapp has been prepared by the Institute and Faculty of Actuaries (IFoA). The IFoA does not accept any responsibility and/or liability whatsoever for the content or use of this webapp. This webapp does not constitute advice and should not be relied upon as such. The IFoA does not guarantee any outcome or result from the application of this webapp and no warranty as to the accuracy or correctness of this webapp is provided."),
                html.Br(),
                html.Div("Copyright: All material in this webapp is the copyright material of the IFoA, unless otherwise stated. Use may be made of this webapp for non-commercial and study/research purposes without permission from the IFoA. Commercial use of this webapp may only be made with the express, prior written permission of the IFoA.")
            ]
        )

Disclaimer_card2 =  dbc.Card(
            [
                html.Div("Note:  above functions will only produce for IfoA datasets which have select slider set to ultimate.  This functionality will be extended soon."),
                html.Br()
            ]
        )


Disclaimer_card3 =  dbc.Card(
            [
                html.Div("Note:  above charts are not yet linked up to the Dataset controls"),
                html.Br()
            ]
        )




#------------------------------------------------------------------------------------
#                              CALLBACK FUNCTIONS
#------------------------------------------------------------------------------------
# we have 5 callback functions.  3 of them relate to changes that occur when the datasource is updated and also the table description are updated.  the inputs are these 2 aforementioned items.  
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
    #print("def update_table1_options_from_dsource has been called {}".format(datetime.now()))
    if dsource is not None:
        if dsource_dropdown_options[dsource-1]['label'] == 'IfoA 00 Series':
            return get_table_description_list_from_datasource(dsource_dropdown_options[dsource-1]['label']),{'display': 'none'}
        elif dsource_dropdown_options[dsource-1]['label'] == 'Human Mortality Database':
            return get_table_description_list_from_datasource(dsource_dropdown_options[dsource-1]['label']),{'display': 'block'}
        elif dsource_dropdown_options[dsource-1]['label'] == 'IfoA 92 Series':
            return get_table_description_list_from_datasource(dsource_dropdown_options[dsource-1]['label']),{'display': 'none'}
        else:
            year_block_1 = {'display': 'none'}
            return [{'label': 'ONS tables to be added Q1 2023'},year_block_1]
    return {'label': 'Choose Datasource'},{'display': 'none'}

@app.callback(
    [dash.dependencies.Output('description_dropdown_2', 'options'),Output(component_id='year_block_2', component_property='style')],
    [dash.dependencies.Input('dsource_dropdown_2', 'value'),dash.dependencies.Input('description_dropdown_2', 'value')]
)
def update_table2_options_from_dsource(dsource,descrip):
    #print("def update_table2_options_from_dsource has been called at {}".format(datetime.now()))  
    if dsource is not None:
        if dsource_dropdown_options[dsource-1]['label'] == 'IfoA 00 Series':
            return get_table_description_list_from_datasource(dsource_dropdown_options[dsource-1]['label']),{'display': 'none'}
        elif dsource_dropdown_options[dsource-1]['label'] == 'Human Mortality Database':
            return get_table_description_list_from_datasource(dsource_dropdown_options[dsource-1]['label']),{'display': 'block'}
        elif dsource_dropdown_options[dsource-1]['label'] == 'IfoA 92 Series':
            return get_table_description_list_from_datasource(dsource_dropdown_options[dsource-1]['label']),{'display': 'none'}
        else:
            year_block_2 = {'display': 'none'}
            return [{'label': 'ONS tables to be added Q1 2023'},year_block_2]
    return {'label': 'Choose Datasource'},{'display': 'none'}

@app.callback(
    [dash.dependencies.Output('description_dropdown_3', 'options'),Output(component_id='year_block_3', component_property='style')],
    [dash.dependencies.Input('dsource_dropdown_3', 'value'),dash.dependencies.Input('description_dropdown_3', 'value')]
)
def update_table3_options_from_dsource(dsource,descrip):
    #print("def update_table3_options_from_dsource has been called at {}".format(datetime.now()))
    if dsource is not None:
        if dsource_dropdown_options[dsource-1]['label'] == 'IfoA 00 Series':
            return get_table_description_list_from_datasource(dsource_dropdown_options[dsource-1]['label']),{'display': 'none'}
        elif dsource_dropdown_options[dsource-1]['label'] == 'Human Mortality Database':
            return get_table_description_list_from_datasource(dsource_dropdown_options[dsource-1]['label']),{'display': 'block'}
        elif dsource_dropdown_options[dsource-1]['label'] == 'IfoA 92 Series':
            return get_table_description_list_from_datasource(dsource_dropdown_options[dsource-1]['label']),{'display': 'none'}
        else:
            year_block_3 = {'display': 'none'}
            return [{'label': 'ONS tables to be added Q1 2023'},year_block_3]
    return {'label': 'Choose Datasource'},{'display': 'none'}

#select sliders callback
#ideally we would separate out the outputs in the callback function so that we have one callback function of slider max values, one for figure, one for hiding slider blocks
#callback functions can run in parrallel and it is a good idea to keep them small and taylored to one output (or group of outputs only)
@app.callback(
    [Output(component_id='select_slider_1', component_property='max'),Output(component_id='select_slider_2', component_property='max'),Output(component_id='select_slider_3', component_property='max'),Output(component_id='slider_block_1', component_property='style'),Output(component_id='slider_block_2', component_property='style'),Output(component_id='slider_block_3', component_property='style')],
    [dash.dependencies.Input('description_dropdown_1', 'value'),
     dash.dependencies.Input('description_dropdown_2', 'value'),
     dash.dependencies.Input('description_dropdown_3', 'value')])
def update_select_sliders(descrip1,descrip2,descrip3):   
    select_rates_slider_blocks=display_select_slider(descrip1,descrip2,descrip3)
    return (select_rates_slider_blocks[0],select_rates_slider_blocks[1],select_rates_slider_blocks[2],select_rates_slider_blocks[3],select_rates_slider_blocks[4],select_rates_slider_blocks[5])


#ideally we would separate out the outputs in the callback function so that we have one callback function of slider max values, one for figure, one for hiding slider blocks
#callback functions can run in parrallel and it is a good idea to keep them small and taylored to one output (or group of outputs only)
@app.callback(
    [Output(component_id='graph', component_property='figure')],
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
def update_figure1(chart_type,slider_1,slider_2,slider_3,graph_slider_value,graph_slider_value2,descrip1,descrip2,descrip3,year_slider_1,year_slider_2,year_slider_3):   
    df_dset = get_dataframe_from_description2(descrip1,descrip2,descrip3)
    data = []
    descriptions=[descrip1,descrip2,descrip3]
    year_sliders=[year_slider_1,year_slider_2,year_slider_3]
    durations=duration_headings_from_select_sliders(slider_1,slider_2,slider_3)
    #durations=duration_headings_from_select_sliders(0,0,0)
    for i in range(3):
        if get_table_name_from_description(descriptions[i]) is not None:
            x = get_x_axis_values_from_chosen_dataset(df_dset[i], descriptions[i], year_sliders[i])
            y = get_y_axis_values_from_chosen_dataset(df_dset[i], descriptions[i], durations[i], year_sliders[i])
            if chart_type == 'line':
                add_trace_to_figure_data(data, x, y, descriptions[i], i+1, "line")
            elif chart_type == 'bar':
                add_trace_to_figure_data(data, x, y, descriptions[i], i+1, "bar")
    #ensuring that no graph lines are shown on initial load
    if descrip1 == None and descrip2 == None and descrip3 == None :
        data=[]
    #create figure
    fig = go.Figure(data=data) 
    set_figure_titles(fig,"Age???","q???")
    set_figure_grid_white(fig)
    set_figure_axis_range(fig,graph_slider_value,graph_slider_value2)
    #print(fig)
    return [fig]


#callback function for when the life office functions tab is selected
@app.callback(
    Output(component_id='graph2', component_property='figure'), 
    [Input("tabs", "value"),
    Input(component_id='select_slider_1', component_property='max'),
    Input(component_id='select_slider_1', component_property='value'),
    Input(component_id='select_slider_2', component_property='max'),
    Input(component_id='select_slider_2', component_property='value'),
    Input(component_id='select_slider_3', component_property='max'),
    Input(component_id='select_slider_3', component_property='value'),
    # Input(component_id='select_slider_2', component_property='value'),
    # Input(component_id='select_slider_3', component_property='value'),
    # Input(component_id='graph_slider', component_property='value'),
    # Input(component_id='graph_slider2', component_property='value'),
    dash.dependencies.Input('description_dropdown_1', 'value'),
    dash.dependencies.Input('year_slider_1', 'value'),
    dash.dependencies.Input('description_dropdown_2', 'value'),
    dash.dependencies.Input('year_slider_2', 'value'),
    dash.dependencies.Input('description_dropdown_3', 'value'),
    dash.dependencies.Input('year_slider_3', 'value'),
    dash.dependencies.Input('int_rate_slider', 'value'),
    # dash.dependencies.Input('year_slider_3', 'value')]
]) 
def update_tab_content(tab,slider_1_max,slider_1,slider_2_max,slider_2,slider_3_max,slider_3,descrip1,year_slider_1,descrip2,year_slider_2,descrip3,year_slider_3,int_rate):
    print(tab)
    if tab == "tab-2":
        print("second tab selected")

    #we need to obtain dataset 1  BTW:  WE WILL WANT TO MOVE TO THE NEW FUNCTION AND DELETE THIS ONE
    df_dset_1 = get_dataframe_from_description(descrip1)
    df_dset_2 = get_dataframe_from_description(descrip2)
    df_dset_3 = get_dataframe_from_description(descrip3)
    #USE SLIDER VALUES TO DETERMINE LOOKUP FIELD VALUE
    #THIS IS ALSO VERY SPECIFIC TO THE 00 SERIES FIELD NAMES
    #AND WOULD PROBABLY BE BEST TAKEN OUT INTO A FUNCTION
    #AND THE CALLBACK FUNCTION MADE MORE GENERALISED FOR ALL DATASETS
    duration_dset_1 = "Duration "+ str(slider_1)
    duration_dset_2 = "Duration "+ str(slider_2)
    duration_dset_3 = "Duration "+ str(slider_3)


 #we don't want to calculate any annuity functions unless maximum select period is chosen. we therefore need a function to check maximum select period
 #we will move the code below into a function
 #because this check will not be relevant if we have a dataset that does not have 
 #select rates
    df=pd.DataFrame()
    if slider_1_max:
        if slider_1 == slider_1_max[0]:
            #newdf to feed into function
            s1 = get_x_axis_values_from_chosen_dataset(df_dset_1,descrip1,year_slider_1)
            s2 = get_y_axis_values_from_chosen_dataset(df_dset_1,descrip1,duration_dset_1,year_slider_1)
            df = pd.concat([s1, s2], axis=1)
            df = df.rename(columns={df.columns[1]: "Rates"})
            df = annuity_series(df,int_rate)

    df2=pd.DataFrame()
    if slider_2_max:
        if slider_2 == slider_2_max[0]:
            #newdf to feed into function
            s1 = get_x_axis_values_from_chosen_dataset(df_dset_2,descrip2,year_slider_2)
            s2 = get_y_axis_values_from_chosen_dataset(df_dset_2,descrip2,duration_dset_2,year_slider_2)
            df2 = pd.concat([s1, s2], axis=1)
            df2 = df2.rename(columns={df2.columns[1]: "Rates"})
            df2 = annuity_series(df2,int_rate)

    df3=pd.DataFrame()
    if slider_3_max:
        if slider_3 == slider_3_max[0]:
            #newdf to feed into function
            s1 = get_x_axis_values_from_chosen_dataset(df_dset_3,descrip3,year_slider_3)
            s2 = get_y_axis_values_from_chosen_dataset(df_dset_3,descrip3,duration_dset_3,year_slider_3)
            df3 = pd.concat([s1, s2], axis=1)
            df3 = df3.rename(columns={df3.columns[1]: "Rates"})
            df3 = annuity_series(df3,int_rate)


    #we now want to set the values of our graph2 figure
    data2 = []

    if get_table_name_from_description(descrip1) is not None:
        if df.empty == False:
            add_trace_to_figure_data(data2,df['Age x'],df['Result'],descrip1,1,"line")

    if get_table_name_from_description(descrip2) is not None:
        if df2.empty == False:
            add_trace_to_figure_data(data2,df2['Age x'],df2['Result'],descrip2,2,"line")

    if get_table_name_from_description(descrip3) is not None:
        if df3.empty == False:
            add_trace_to_figure_data(data2,df3['Age x'],df3['Result'],descrip3,3,"line")
    

    if data2 == []:
        trace_1 = go.Scatter(x=[0], y=[0])
        data2.append(trace_1)



    fig2 = go.Figure(data=data2)

    set_figure_titles(fig2,"Age???","a???")
    set_figure_axis_range(fig2,[0,120],[0,30])
    set_figure_grid_white(fig2)

    fig2.update_layout(title='PV of ??1 annuity due')
 
                     

    return fig2



# --------------------------------------------------------------------------------------
#                   SET THE LAYOUT OF THE APP
#---------------------------------------------------------------------------------------

fred = html.Div([dataset1_card, dataset2_card, dataset3_card],style={'overflow-y': 'scroll', 'height': '100%'})

# Calculate the height of blue_card in pixels
blue_card_height = 10  # Replace with the actual height of blue_card
offset_value = str(blue_card_height) + "px"

column1 = dbc.Col([blue_card,fred ],width=4,style={'background-color': '#F3F5F7'})
    

column2 = dbc.Col(
    [
        html.Div([
                    dcc.Tabs(id='tabs',children=[
                                dcc.Tab(label='Age Specific Rates',
                                        children =
                                                    [
                                                                html.Div(style={"height": offset_value}), type_of_graph_card,html.Div(style={"height": offset_value}),output_card,html.Div(style={"height": offset_value}),html.Div(style={"height": offset_value}),Disclaimer_card
                                                    ]
                                
                                
                                                                            ),
                                dcc.Tab(label='Life Office Functions',
                                                     children =
                                                    [
                                                                html.Div(style={"height": offset_value}), #type_of_graph_card,
                                                                dcc.Loading(
                    id="ls-loading-2",
                    children=[html.Div(style={"height": offset_value}),output_card2],
                    type="circle",
                )
                                                                ,html.Div(style={"height": offset_value}),html.Div(style={"height": offset_value}),Disclaimer_card2
                                                    ]
                                
                                                                            ),
                                dcc.Tab(label='3D',
                                
                                children =
                                            [output_card3,Disclaimer_card3 
                                                


                                            ]
                                
                                
                                ),
                                                            ])
                                        ]), 

        
    ],
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







