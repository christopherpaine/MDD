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

# Initialize the app
app = dash.Dash()

# Create a plotly figure
fig = px.line(df, x='Age x', y='Duration 0')

# Create a Dash layout
app.layout = html.Div([
    dcc.Graph(figure=fig)
])

# Run the app
if __name__ == '__main__':
    app.run_server()







