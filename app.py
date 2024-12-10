import dash
from dash import dcc, html, Input, Output
import pandas as pd
import sqlite3
import dash_table

# Initialize the Dash app
app = dash.Dash()

# CSV file path
CSV_FILE = "UMN.csv"

# SQLite Database setup
def create_db():
    # Read data from CSV
    df = pd.read_csv(CSV_FILE)

    # Create SQLite database and populate it with CSV data
    conn = sqlite3.connect('issues.db')
    df.to_sql('issues', conn, if_exists='replace', index=False)  # Replace any existing table with the CSV data
    conn.close()

create_db()

# Function to fetch data from the database
def fetch_data(building_filter=None):
    conn = sqlite3.connect('issues.db')
    query = "SELECT * FROM issues"
    
    if building_filter:
        query += f" WHERE Building = '{building_filter}'"
        
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Function to fetch unique buildings from the table
def fetch_buildings():
    conn = sqlite3.connect('issues.db')
    query = "SELECT DISTINCT Building FROM issues"
    df = pd.read_sql(query, conn)
    conn.close()
    return df['Building'].tolist()

# List of issues for the Issue dropdown
ISSUES = [
    "Mobility", "Wheelchair Access", "Visual Assistance", "Audio Assistance", "Elevator Access", "Other"
]

# Dash layout
app.layout = html.Div([
    html.H1("Inclusive UMN Dashboard", style={'textAlign': 'center', 'color': '#2c3e50'}),

    # Search bar dropdown for building (dynamically populated from table)
    html.Div([
        html.Label('Search by Building'),
        dcc.Dropdown(
            id='building-search',
            options=[{'label': building, 'value': building} for building in fetch_buildings()],
            placeholder="Select a Building to Search",
            style={'margin': '5px', 'width': '40%'}
        )
    ], style={'marginBottom': '20px'}),

    html.Div([
        dash_table.DataTable(
            id='issues-table',
            columns=[
                {'name': 'Building', 'id': 'Building'},
                {'name': 'Issue', 'id': 'Issue'},
                {'name': 'Description', 'id': 'Description'},
                {'name': 'Verified', 'id': 'Verified'}
            ],
            data=fetch_data().to_dict('records'),
            style_table={'height': '400px', 'overflowY': 'auto'},
            style_header={
                'backgroundColor': '#2c3e50',
                'color': 'white',
                'fontWeight': 'bold',
                'textAlign': 'center'
            },
            style_cell={
                'textAlign': 'center',  # Center text in all cells
                'padding': '5px'
            }
        )
    ], style={'marginBottom': '20px'}),

    html.Div([
        html.H4("Add a New Issue", style={'color': '#2c3e50'}),
        dcc.Dropdown(
            id='building',
            options=[{'label': building, 'value': building} for building in fetch_buildings()],
            placeholder="Select a Building",
            style={'margin': '5px', 'width': '40%'}
        ),
        dcc.Dropdown(
            id='issue',
            options=[{'label': issue, 'value': issue} for issue in ISSUES],
            placeholder="Select an Issue",
            style={'margin': '5px', 'width': '40%'}
        ),
        dcc.Input(id='description', type='text', placeholder='Description', style={'margin': '5px', 'width': '40%'}),
        html.Button('Add Issue', id='add-button', n_clicks=0,
                    style={'backgroundColor': '#2c3e50', 'color': 'white', 'padding': '10px 20px', 'marginTop': '10px'})
    ], style={'padding': '20px', 'border': '1px solid #ddd', 'borderRadius': '10px', 'backgroundColor': '#f9f9f9'}),

    html.Div(id='form-feedback', style={'marginTop': '10px', 'color': '#27ae60'})
])

# Combined callback to update the table
@app.callback(
    Output('issues-table', 'data'),
    [Input('building-search', 'value'),
     Input('add-button', 'n_clicks')],
    [Input('building', 'value'), Input('issue', 'value'), Input('description', 'value')]
)
def update_table(building, n_clicks, building_input, issue, description):
    ctx = dash.callback_context

    # Check which input triggered the callback
    if ctx.triggered:
        input_id = ctx.triggered[0]['prop_id'].split('.')[0]

    # If building search is triggered, filter the data based on building
    if input_id == 'building-search' and building:
        filtered_data = fetch_data(building_filter=building)
        return filtered_data.to_dict('records')

    # If Add Issue button is clicked, add a new issue and update the table
    elif input_id == 'add-button' and n_clicks > 0 and building_input and issue and description:
        conn = sqlite3.connect('issues.db')
        c = conn.cursor()
        # Insert the new issue with "Verified" set to "No" by default
        c.execute("INSERT INTO issues (Building, Issue, Description, Verified) VALUES (?, ?, ?, ?)",
                  (building_input, issue, description, "No"))
        conn.commit()
        conn.close()
        updated_data = fetch_data().to_dict('records')
        return updated_data
    else:
        return fetch_data().to_dict('records')


if __name__ == '__main__':
    app.run_server(debug=True)

