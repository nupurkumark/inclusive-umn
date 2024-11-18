from dash import Dash, html, dcc, Input, Output, State
from dash.dash_table import DataTable
import dash_bootstrap_components as dbc
import pandas as pd
from data_manager import get_data, add_record

# Initialize the app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Load the full data to get unique building names for the dropdown
full_df = get_data('full_data')  # Make sure to use the correct table name

# Define the layout
app.layout = html.Div([
    html.H1("Inclusive UMN Dashboard"),

    # Dropdown for filtering by building
    dcc.Dropdown(
        options=[{'label': building, 'value': building} for building in full_df['Building'].unique()],
        placeholder="Select a Building",
        id='dropdown-selection'
    ),

    # Styled DataTable
    DataTable(
        id='combined-table',
        columns=[
            {'name': 'Building', 'id': 'Building'},
            {'name': 'Event', 'id': 'Event'},
            {'name': 'User', 'id': 'User'}
        ],
        style_data={  # Style individual data cells
            'whiteSpace': 'normal',
            'height': 'auto',
            'textAlign': 'center',  # Center-align text
            'backgroundColor': '#f9f9f9',
        },
        style_header={  # Style header cells
            'backgroundColor': '#4e73df',
            'fontWeight': 'bold',
            'color': 'white',
            'textAlign': 'center',
        },
        style_table={  # Table-level styling
            'overflowX': 'auto',
            'border': '1px solid #dee2e6',
        },
    ),

    # Button to open form for new record entry
    html.Button("Add New Record", id="add-record-button", n_clicks=0),
    dcc.Location(id='form-redirect', refresh=True),
    
    # Form to add new records, hidden initially
    dbc.Collapse(
        dbc.Form([
            dbc.Label("Building"),
            dbc.Input(id="input-building", type="text"),
            dbc.Label("Event"),
            dbc.Input(id="input-event", type="text"),
            dbc.Label("User"),
            dbc.Input(id="input-user", type="text"),
            dbc.Button("Submit", id="submit-form", n_clicks=0)
        ]),
        id="form-container", is_open=False
    )
])

# Callback to toggle form visibility
@app.callback(
    Output('form-container', 'is_open'),
    [Input('add-record-button', 'n_clicks')],
    [State('form-container', 'is_open')]
)
def toggle_form(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open

# Callback to update the combined table based on dropdown and form inputs
@app.callback(
    Output('combined-table', 'data'),
    Input('dropdown-selection', 'value'),
    Input('submit-form', 'n_clicks'),
    State('input-building', 'value'),
    State('input-event', 'value'),
    State('input-user', 'value')
)
def update_combined_table(selected_building, n_clicks, building, event, user):
    # Add new record if form is submitted
    if n_clicks:
        add_record(building, event, user)
    
    # Fetch updated data
    df = get_data('full_data')  # Use 'full_data' or correct table name

    # Filter by selected building if a building is selected
    if selected_building:
        df = df[df['Building'] == selected_building]
    
    # Convert data to dictionary format for DataTable
    return df.to_dict('records')

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)


