from dash import Dash, html, dcc, Input, Output, State, callback_context
import dash_bootstrap_components as dbc
from dash.dash_table import DataTable
from data_manager import get_data, add_record

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)

# Load initial data
full_df = get_data('full_data')

def main_page():
    return html.Div([
        dcc.Dropdown(
            options=[{'label': building, 'value': building} for building in full_df['Building'].unique()],
            placeholder="Select a Building",
            id='dropdown-selection'
        ),
        DataTable(
            id='combined-table',
            data=full_df.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in full_df.columns],
            style_data={'whiteSpace': 'normal', 'height': 'auto', 'textAlign': 'center', 'backgroundColor': '#f9f9f9'},
            style_header={'backgroundColor': '#4e73df', 'fontWeight': 'bold', 'color': 'white', 'textAlign': 'center'},
            style_table={'overflowX': 'auto', 'border': '1px solid #dee2e6'}
        ),
        dcc.Link("Add New Record", href="/add-record")
    ])

def add_record_form():
    return html.Div([
        html.H2("Add New Record"),
        dbc.Form([
            dbc.Label("Building"),
            dbc.Input(id="input-building", type="text"),
            dbc.Label("Event"),
            dbc.Input(id="input-event", type="text"),
            dbc.Label("User"),
            dbc.Input(id="input-user", type="text"),
            dbc.Label("Issues"),
            dbc.Select(
                id="input-issues",
                options=[
                    {"label": "Wheelchair Access", "value": "wheelchair_access"},
                    {"label": "Visual Assistance", "value": "visual_assistance"},
                    {"label": "Audio Assistance", "value": "audio_assistance"},
                    {"label": "Elevator Access", "value": "elevator_access"},
                    {"label": "Other", "value": "other"}
                ],
                placeholder="Select an accessibility issue"
            ),
            dbc.Button("Submit", id="submit-form", n_clicks=0),
            dcc.Link("Back to Home", href="/")  # Link to go back to the main page
        ])
    ])

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.H1("Inclusive UMN Dashboard"),
    html.Div(id='content')
])

# Callback to update the page based on URL path
@app.callback(
    Output('content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    if pathname == '/add-record':
        return add_record_form()
    return main_page()

# Separate callback to handle form submission and redirect back to main page
@app.callback(
    Output('url', 'pathname'),
    Input('submit-form', 'n_clicks'),
    [State('input-building', 'value'),
     State('input-event', 'value'),
     State('input-user', 'value'),
     State('input-issues', 'value')]
)
def handle_form_submission(n_clicks, building, event, user, issues):
    if n_clicks:
        add_record(building, event, user, issues)  # Add record to the database
        global full_df
        full_df = get_data('full_data')  # Reload updated data
        return '/'  # Redirect to main page
    return dash.no_update

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
