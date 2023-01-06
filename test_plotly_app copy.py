# Import the MySQL connector
import mysql.connector
import pandas as pd

# Connect to the MySQL server
#cnx = mysql.connector.connect(user='root', password='ActuarialDashboard', host='ELITEBOOK', database='mydb')
cnx = mysql.connector.connect(user='Christopher Paine', password='ActuarialDashboard', host='ELITEBOOK', database='mydb')
print(cnx)

# Create a cursor object to execute SQL statements
cursor = cnx.cursor()

# Execute a SQL SELECT statement to retrieve data from the database
query = "SELECT * FROM AMC00"
#cursor.execute(query)

# populate dataframe by sql
df = pd.read_sql(query,con=cnx)

#print what has been retrieved
print(df.head)

# Close the cursor and connection when you are finished
cursor.close()
cnx.close()


#-------------------------------------------------------------
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px

# Initialize the app
app = dash.Dash()

# Create a plotly figure
fig = px.line(df, x='Age', y='q_[x]')

# Create a Dash layout
app.layout = html.Div([
    dcc.Graph(figure=fig)
])

# Run the app
if __name__ == '__main__':
    app.run_server()







