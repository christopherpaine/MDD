#----------------------------------------------------------------------------------------
#                      LOAD IN THE DATA
#---------------------------------------------------------------------------------------------
# Import the MySQL connector
import mysql.connector
import pandas as pd

# Load the data
df = pd.read_excel('Mortality_tables/ams00.xls')

#print what has been retrieved
print(df.head)

#-------------------------------------------------------------
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from dash.dependencies import Input, Output
import dash_daq as daq
from layout_components import get_slider
import dash_bootstrap_components as dbc
#--------------------------------------------------------------------------

# Initialize the app
app = dash.Dash()
server = app.server

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

#-------------------------------------------------------------------------------------
#           CREATE SOME CARD OBJECTS
#-------------------------------------------------------------------------------------

blue_card = dbc.Card(
            [
                html.H4("Mortality Data Dashboard", className="card-title", style={'color': '#C3941E'}),
                html.P("Exploration of Open Source Datasets", className="card-text", style={'color': '#FFFFFF'}),
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
                                            dcc.Dropdown(id='dropdown',options=[{'label': 'IfoA 00 Series', 'value': 1},{'label': 'Human Mortality Database', 'value': 2},{'label': 'Office National Statistics', 'value': 3}],value=1),
                                            html.Br(),
                                            dbc.Label("Table"),
                                            dcc.Dropdown(id='dropdown',options=[{'label': 'Option 1', 'value': 1},{'label': 'Option 2', 'value': 2},{'label': 'Option 3', 'value': 3}],value=1),
                                            html.Br(),
                                            dbc.Label("Number of Select Years"),
                                            dcc.Slider(min=0, max=5, value=5, marks={i: str(i) for i in range(6)})
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
                                            dcc.Dropdown(id='dropdown',options=[{'label': 'IfoA 00 Series', 'value': 1},{'label': 'Human Mortality Database', 'value': 2},{'label': 'Office National Statistics', 'value': 3}],value=1),
                                            html.Br(),
                                            dbc.Label("Table"),
                                            dcc.Dropdown(id='dropdown',options=[{'label': 'Option 1', 'value': 1},{'label': 'Option 2', 'value': 2},{'label': 'Option 3', 'value': 3}],value=1),
                                            html.Br(),
                                            dbc.Label("Number of Select Years"),
                                            dcc.Slider(min=0, max=5, value=5, marks={i: str(i) for i in range(6)})
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
                                            dcc.Dropdown(id='dropdown',options=[{'label': 'IfoA 00 Series', 'value': 1},{'label': 'Human Mortality Database', 'value': 2},{'label': 'Office National Statistics', 'value': 3}],value=1),
                                            html.Br(),
                                            dbc.Label("Table"),
                                            dcc.Dropdown(id='dropdown',options=[{'label': 'AMC00 Permanent Assurances Males', 'value': 1},{'label': 'Option 2', 'value': 2},{'label': 'Option 3', 'value': 3}],value=1),
                                            html.Br(),
                                            dbc.Label("Number of Select Years"),
                                            dcc.Slider(min=0, max=5, value=5, marks={i: str(i) for i in range(6)})
                                ]
                            )
                        ]

                        )

type_of_graph_card = dbc.Card(
    [
        dbc.Row(
            [
                dbc.Col(html.B("Chart Type"), width=2,style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}),
                dbc.Col(dcc.Dropdown(id='dropdown', options=[{'label': 'Line', 'value': 1}, {'label': 'Bar', 'value': 2}], value=1), width=10)
            ]
        )
    ]
)

 


output_card = dbc.Card(
            [
                dcc.Graph(figure={"data": [{"x": [1, 2, 3], "y": [1, 2, 3]}]}),
                dcc.Slider(
                    min=0, max=10, value=5, marks={i: str(i) for i in range(11)}
                ),
                html.A(
                    "Download Data",
                    id="download-link",
                    download="rawdata.csv",
                    href="",
                    target="_blank",
                ),
            ]
        )


Disclaimer_card =  dbc.Card(
            [
                html.Div("Disclaimer: This document has been prepared by the Institute and Faculty of Actuaries (IFoA). The IFoA does not accept any responsibility and/or liability whatsoever for the content or use of this document. This document does not constitute advice and should not be relied upon as such. The IFoA does not guarantee any outcome or result from the application of this document and no warranty as to the accuracy or correctness of this document is provided."),
                html.Br(),
                html.Div("Copyright: All material in this document is the copyright material of the IFoA, unless otherwise stated. Use may be made of these pages for non-commercial and study/research purposes without permission from the IFoA. Commercial use of this material may only be made with the express, prior written permission of the IFoA.")
            ]
        )




# 











# Calculate the height of blue_card in pixels
blue_card_height = 10  # Replace with the actual height of blue_card
offset_value = str(blue_card_height) + "px"

column1 = dbc.Col(
    [blue_card, dataset1_card, dataset2_card, dataset3_card],
    width=4,
    style={'background-color': '#F3F5F7'}
)

column2 = dbc.Col(
    [html.Div(style={"height": offset_value}), type_of_graph_card,html.Div(style={"height": offset_value}),output_card,html.Div(style={"height": offset_value}),Disclaimer_card],
    width=8,
    style={'background-color': '#F3F5F7'}
)

app.layout = html.Div(
    [
        dbc.Row([column1, column2]),
    ]
)



#---------------------------------------------------------------------------------------
# Run the app
if __name__ == '__main__':
    app.run_server()







