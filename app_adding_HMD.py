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
df_filtered = df_table_summary[df_table_summary['Datasource'] == 'IfoA 00 Series']
table_descriptions = df_filtered['Table Description'].tolist()






#-----------------------------------------------------------------------------------
#                       OBJECTS FOR GRAPH
#---------------------------------------------------------------------------------


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
                                            dcc.Dropdown(id='dsource_dropdown_1',options=dsource_dropdown_options,value=1,style={'font-size':'12px'}),
                                            html.Br(),
                                            dbc.Label("Description"),
                                            html.Br(),
                                            dcc.Dropdown(id='description_dropdown_1',options=options_dd_1,value=None,placeholder='Please Select',style={'font-size':'12px'}),                                            
                                            html.Br(),
                                            html.B("  "),
                                            dbc.Label("Table"),
                                            dcc.Dropdown(id='table_dropdown_1',options=options_td_1,value=None,placeholder='Please Select',style={'font-size':'12px'}),
                                            html.Br(),
                                            html.Div([
                                                dbc.Label("Number of Select Years (max = ultimate)"),
                                                dcc.Slider(id='select_slider_1',min=0, max=5, value=0,step=1, marks={i: str(i) for i in range(1,6)})
                                            ], style= {'display': 'none'},id='slider_block_1'),
                                            html.Div([
                                                dbc.Label("Year"),
                                                dcc.Slider(id='year_slider_1',min=1920, max=2020, value=2020,step=1, marks={i: str(i) for i in range(1920,2020,10)})
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
                                            dcc.Dropdown(id='dsource_dropdown_2',options=dsource_dropdown_options,value=1,style={'font-size':'12px'}),
                                            html.Br(),
                                            dbc.Label("Description"),
                                            html.Br(),
                                            dcc.Dropdown(id='description_dropdown_2',options=options_dd_2,value=None,placeholder='Please Select',style={'font-size':'12px'}),                                            
                                            html.Br(),
                                            html.B("  "),
                                            dbc.Label("Table"),
                                            dcc.Dropdown(id='table_dropdown_2',options=[],value=None,style={'font-size':'12px'}),
                                            html.Br(),
                                            html.Div([
                                                dbc.Label("Number of Select Years (max = ultimate)"),
                                                dcc.Slider(id='select_slider_2',min=0, max=5, value=0,step=1, marks={i: str(i) for i in range(6)})
                                            ], style= {'display': 'none'},id='slider_block_2'),
                                            html.Div([
                                                dbc.Label("Year"),
                                                dcc.Slider(id='year_slider_2',min=1920, max=2020, value=2020,step=1, marks={i: str(i) for i in range(1920,2020,10)})
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
                                            dcc.Dropdown(id='dsource_dropdown_3',options=dsource_dropdown_options,value=1,style={'font-size':'12px'}),
                                            html.Br(),
                                            dbc.Label("Description"),
                                            html.Br(),
                                            dcc.Dropdown(id='description_dropdown_3',options=options_dd_1,value=None,placeholder='Please Select',style={'font-size':'12px'}),                                            
                                            html.Br(),
                                            html.B("  "),
                                            
                                            dbc.Label("Table"),
                                            dcc.Dropdown(id='table_dropdown_3',options=[],value=None,style={'font-size':'12px'}),
                                            html.Br(),
                                            html.Div([
                                                dbc.Label("Number of Select Years (max = ultimate)"),
                                                dcc.Slider(id='select_slider_3',min=0, max=5, value=0,step=1, marks={i: str(i) for i in range(6)})
                                            ], style= {'display': 'none'},id='slider_block_3'), 
                                            html.Div([
                                                dbc.Label("Year"),
                                                dcc.Slider(id='year_slider_3',min=1920, max=2020, value=2020,step=1, marks={i: str(i) for i in range(1920,2020,10)})
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

@app.callback(
    [dash.dependencies.Output('table_dropdown_1', 'options'),dash.dependencies.Output('description_dropdown_1', 'options'),Output(component_id='year_block_1', component_property='style')],
    [dash.dependencies.Input('dsource_dropdown_1', 'value'),dash.dependencies.Input('description_dropdown_1', 'value')]
)
def update_table1_options_from_dsource(dsource,descrip):
    #print("dsource is:"+str(dsource))
    print("called")
    if dsource == 1:
        print(descrip)
        #lookup description in df_table_summary to get table name
        df_filtered2 = df_table_summary[df_table_summary['Table Description'] == descrip]
        df_filtered3 = df_filtered2['Table'].tolist()
        print(df_filtered3)
        year_block_1 = {'display': 'none'}
        return df_filtered3, table_descriptions,year_block_1
    elif dsource == 2:
        year_block_1 = {'display': 'block'}
        return [{'label': 'HMD tables to be added Q1 2023'},{'label': 'HMD tables to be added Q1 2023'},year_block_1]
    else:
        year_block_1 = {'display': 'none'}
        return [{'label': 'ONS tables to be added Q1 2023'},{'label': 'ONS tables to be added Q1 2023'},year_block_1]

@app.callback(
    [dash.dependencies.Output('table_dropdown_2', 'options'),dash.dependencies.Output('description_dropdown_2', 'options'),Output(component_id='year_block_2', component_property='style')],
    [dash.dependencies.Input('dsource_dropdown_2', 'value'),dash.dependencies.Input('description_dropdown_2', 'value')]
)
def update_table2_options_from_dsource(dsource,descrip):
    #print("dsource is:"+str(dsource))
    print("called")
    if dsource == 1:
        print(descrip)
        #lookup description in df_table_summary to get table name
        df_filtered2 = df_table_summary[df_table_summary['Table Description'] == descrip]
        df_filtered3 = df_filtered2['Table'].tolist()
        print(df_filtered3)
        year_block_2 = {'display': 'none'}
        return df_filtered3, table_descriptions,year_block_2
    elif dsource == 2:
        year_block_2 = {'display': 'block'}
        return [{'label': 'HMD tables to be added Q1 2023'},{'label': 'HMD tables to be added Q1 2023'},year_block_2]
    else:
        year_block_2 = {'display': 'none'}
        return [{'label': 'ONS tables to be added Q1 2023'},{'label': 'ONS tables to be added Q1 2023'},year_block_2]


@app.callback(
    [dash.dependencies.Output('table_dropdown_3', 'options'),dash.dependencies.Output('description_dropdown_3', 'options'),Output(component_id='year_block_3', component_property='style')],
    [dash.dependencies.Input('dsource_dropdown_3', 'value'),dash.dependencies.Input('description_dropdown_3', 'value')]
)
def update_table3_options_from_dsource(dsource,descrip):
    #print("dsource is:"+str(dsource))
    #print("called")
    if dsource == 1:
        print(descrip)
        #lookup description in df_table_summary to get table name
        df_filtered2 = df_table_summary[df_table_summary['Table Description'] == descrip]
        df_filtered3 = df_filtered2['Table'].tolist()
        print(df_filtered3)
        year_block_3 = {'display': 'none'}
        return df_filtered3, table_descriptions,year_block_3
    elif dsource == 2:
        year_block_3 = {'display': 'block'}
        return [{'label': 'HMD tables to be added Q1 2023'},{'label': 'HMD tables to be added Q1 2023'},year_block_3]
    else:
        year_block_3 = {'display': 'none'}
        return [{'label': 'ONS tables to be added Q1 2023'},{'label': 'ONS tables to be added Q1 2023'},year_block_3]


@app.callback(
    [Output(component_id='graph', component_property='figure'),Output(component_id='select_slider_1', component_property='max'),Output(component_id='select_slider_2', component_property='max'),Output(component_id='select_slider_3', component_property='max'),Output(component_id='slider_block_1', component_property='style'),Output(component_id='slider_block_2', component_property='style'),Output(component_id='slider_block_3', component_property='style')],
    [Input(component_id='table_dropdown_1', component_property='value'),
     Input(component_id='table_dropdown_2', component_property='value'),
     Input(component_id='table_dropdown_3', component_property='value'),
     Input(component_id='chart_type_dropdown', component_property='value'),
     Input(component_id='select_slider_1', component_property='value'),
     Input(component_id='select_slider_2', component_property='value'),
     Input(component_id='select_slider_3', component_property='value'),
     Input(component_id='graph_slider', component_property='value'),
     Input(component_id='graph_slider2', component_property='value')]
)
def update_figure(sheet_name1, sheet_name2, sheet_name3, chart_type,slider_1,slider_2,slider_3,graph_slider_value,graph_slider_value2):
    df_dset_1 = pd.read_excel('Mortality_tables/00series.xls', sheet_name=sheet_name1)
    df_dset_2 = pd.read_excel('Mortality_tables/00series.xls', sheet_name=sheet_name2)
    df_dset_3 = pd.read_excel('Mortality_tables/00series.xls', sheet_name=sheet_name3)
    data = []

    duration_dset_1 = "Duration "+ str(slider_1)
    print("duration dset 1 is:"+str(duration_dset_1))
    duration_dset_2 = "Duration "+ str(slider_2)
    print("duration dset 2 is:"+str(duration_dset_2))
    duration_dset_3 = "Duration "+ str(slider_3)
    print("duration dset 3 is:"+str(duration_dset_3))

    #lookup max select years in df_table_summary to get table name
    df_filtered2 = df_table_summary[df_table_summary['Table'] == sheet_name1]
    df_filtered3 = df_filtered2['Select Years'].tolist()
    print("max select years for dset 1")
    print(df_filtered3)
    max_select_dset_1 = df_filtered3 

    df_filtered2 = df_table_summary[df_table_summary['Table'] == sheet_name2]
    df_filtered3 = df_filtered2['Select Years'].tolist()
    print("max select years for dset 2")
    print(df_filtered3)
    max_select_dset_2 = df_filtered3

    df_filtered2 = df_table_summary[df_table_summary['Table'] == sheet_name3]
    df_filtered3 = df_filtered2['Select Years'].tolist()
    print("max select years for dset 3")
    print(df_filtered3)
    max_select_dset_3 = df_filtered3 


    print("graph slider value")
    print(graph_slider_value)

    

    if sheet_name1 is not None:
        if chart_type == 'line':
            trace_1 = go.Scatter(x=df_dset_1['Age x'], y=df_dset_1[duration_dset_1], name=sheet_name1, marker=dict(color="#abe2fb"))
        elif chart_type == 'bar':
            trace_1 = go.Bar(x=df_dset_1['Age x'], y=df_dset_1[duration_dset_1 ], name=sheet_name1, marker=dict(color="#abe2fb"))
        data.append(trace_1)


    if sheet_name2 is not None:
        if chart_type == 'line':
            trace_2 = go.Scatter(x=df_dset_2['Age x'], y=df_dset_2[duration_dset_2], name=sheet_name2,marker=dict(color="#002c53"))
        elif chart_type == 'bar':
            trace_2 = go.Bar(x=df_dset_2['Age x'], y=df_dset_2[duration_dset_2], name=sheet_name2,marker=dict(color="#002c53"))
        data.append(trace_2)

    if sheet_name3 is not None:
        if chart_type == 'line':
            trace_3 = go.Scatter(x=df_dset_3['Age x'], y=df_dset_3[duration_dset_3], name=sheet_name3,marker=dict(color=" #c3941e"))
        elif chart_type == 'bar':
            trace_3 = go.Bar(x=df_dset_3['Age x'], y=df_dset_3[duration_dset_3], name=sheet_name3,marker=dict(color=" #c3941e"))
        data.append(trace_3)


    

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
                    
    #determine which slider blocks to display
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


    return fig,max_select_dset_1,max_select_dset_2,max_select_dset_3,slider_block_1,slider_block_2,slider_block_3



# --------------------------------------------------------------------------------------
#                   SET THE LAYOUT OF THE APP
#---------------------------------------------------------------------------------------

fred = html.Div([dataset1_card, dataset2_card, dataset3_card],style={'overflow-y': 'scroll', 'height': '50%'})

# Calculate the height of blue_card in pixels
blue_card_height = 10  # Replace with the actual height of blue_card
offset_value = str(blue_card_height) + "px"

column1 = dbc.Col([blue_card,fred ],width=4,style={'background-color': '#F3F5F7'})
    

column2 = dbc.Col(
    [html.Div(style={"height": offset_value}), type_of_graph_card,html.Div(style={"height": offset_value}),output_card,html.Div(style={"height": offset_value}),Disclaimer_card],
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







