import dash_bootstrap_components as dbc
from dash import dcc, html, Output, Input, State
from dash.exceptions import PreventUpdate
from apps.dbconnect import create_connection, close_connection
from urllib.parse import parse_qs
import time

def fetch_service_details(patient_id):
    connection = create_connection()
    data = None
    if connection: 
        cursor = connection.cursor()
        query = """
        SELECT patient_first_name, patient_last_name
        FROM patient
        WHERE patient_id = %s
        """
        cursor.execute(query, (patient_id,))
        result = cursor.fetchone()  # Fetch one row from the query result
        if result:
            data = {
                'patient_first_name': result[0],
                'patient_last_name': result[1]
            }
        print(f"Query result: {data}")  # Debugging line
        close_connection(connection)
    return data


def update_patient_details(patient_id, first_name, last_name):
    """
    Updates the patient table with the provided first and last names.
    """
    connection = create_connection()
    if connection:
        try:
            print(f"Updating patient_id: {patient_id} with first_name: {first_name}, last_name: {last_name}")
            cursor = connection.cursor()
            query = """
            UPDATE patient
            SET patient_first_name = %s, patient_last_name = %s
            WHERE patient_id = %s
            """
            cursor.execute(query, (first_name, last_name, patient_id))
            connection.commit()  # Commit the transaction
            print("Database update successful.")
        except Exception as e:
            print(f"Error during database update: {e}")
            raise e  # Re-raise exception for proper debugging
        finally:
            close_connection(connection)
    else:
        print("Error: Unable to establish database connection.")
        raise Exception("Database connection failed.")


# Define styles for the layout
styles = {
    "subHeader1": {
        "padding": "40px",
        "marginLeft": "60px"
    },
    "backMedRecord": {
        "fontSize": "18px",
        "marginTop": "-30px",
        "color": "#05066d"
    },
    "titlePatientInfo": {
        "fontSize": "30px",
        "color": "#05066d",
        "fontWeight": "bold"
    },
    "divider1": {
        "width": "93%",
        "border": "2px solid #05066d",
        "marginTop": "-3px"
    },
}

# Set up routing and layout
layout = html.Div(
    children=[

        # Content
        html.Div(
            style=styles["subHeader1"],
            children=[
                # Section with an image icon link
                html.Div(
                    children=[
                        html.A(
                            [
                                html.Img(
                                    src="/assets/resources/Arrow Icon.png",  # Path to your icon image in the assets folder
                                    style={
                                        "width": "20px", 
                                        "height": "20px", 
                                        "margin-right": "8px", 
                                        "margin-bottom": "3px", 
                                        "vertical-align": "middle"  
                                    },  # Adjust size and alignment
                                ),
                                "Back to Medical Records Page"
                            ],
                            href="/medical_records",  # Link target
                            style={
                                **styles["backMedRecord"],  # Apply existing styles
                                "text-decoration": "none",  # Remove underline
                                "color": "inherit"  # Ensure link text inherits color from parent
                            },
                        ),
                    ],
                    style={"margin-bottom": "50px"},
                ),
                html.H2("Patient Information", style=styles["titlePatientInfo"]),
                html.Hr(style=styles["divider1"]),
            ],
        ),

        # The table box
            html.Div(
            style={"padding": "20px", "margin-top": "-60px"},
            children=[
                # Edit patient record
                html.Div(
                    style={"padding": "20px"},
                    children=[
                        # Table Container with smaller width
                        html.Table(
                            style={
                                "width": "89%",  # Reduced table width
                                "margin-left": "60px",  # Move the table to the left
                                "margin-top": "-15px",
                                "border": "1px solid black", 
                                "border-collapse": "collapse"
                            },
                            children=[
                                # Table Header Row
                                html.Tr(
                                    children=[
                                        html.Th(
                                            children=[
                                                "Edit Patient Record",
                                            ],
                                            style={
                                                "padding": "10px", 
                                                "text-align": "left", 
                                                "font-weight": "bold", 
                                                "background-color": "#05066d", 
                                                "color": "white"
                                            },
                                        )
                                    ],   
                                ),
                           
                            # Table Body Row 
                            html.Tr(
                                style={"border": "1px solid black"},
                                children=[
                                    html.Td(
                                        children=[
                                            # Service Type Label and Input
                                            html.Div(
                                                children=[
                                                    "Patient First Name",
                                                    html.Br(),  # Line break
                                                    dcc.Input(
                                                        id="first-name-type-input-edit-mode",  # ID for the input field
                                                        type="text",  # Type of the input field (text)
                                                        placeholder="Juan",  # Placeholder text for the input
                                                        style={"width": "350px", "padding": "5px", "font-style": "italic"}  # Reduced size for inline display
                                                    ),
                                                ],
                                                style={"text-align": "left", "color": "#05066d", "font-weight": "bold", "margin-right": "10px"},  # Align label and input field
                                            ),

                                            # Service Fee Label and Input
                                            html.Div(
                                                children=[
                                                    "Patient Last Name",
                                                    html.Br(),  # Line break
                                                    dcc.Input(
                                                        id="last-name-input-edit-mode",  # ID for the input field
                                                        type="text",  # Type of the input field (number)
                                                        placeholder="Dela Cruz",  # Placeholder text for the input
                                                        style={"width": "350px", "padding": "5px", "font-style": "italic"}  # Reduced size for inline display
                                                    ),
                                                ],
                                                style={"text-align": "left", "color": "#05066d", "font-weight": "bold", "margin-left": "10px"},  # Align label and input field
                                            ),

                                            # Buttons: Cancel and Add (Aligned to the right)
                                            html.Div(
                                                children=[
                                                    html.A(
                                                        html.Button(
                                                            "Cancel",
                                                            id="cancel-button",
                                                            n_clicks=0,
                                                            style={
                                                                "background-color": "#f44336", 
                                                                "color": "white", 
                                                                "font-size": "14px",
                                                                "font-weight": "bold",
                                                                "padding": "5px 40px", 
                                                                "border-radius": "5px",
                                                                "margin-right": "20px", 
                                                                "margin-top": "40px", 
                                                                "border": "none", 
                                                                "cursor": "pointer"
                                                            }
                                                        ),
                                                        href="/medical_records",  # Replace with the target URL
                                                    ),
                                                    html.Button(
                                                        "Save",
                                                        id="save-button",
                                                        n_clicks=0,
                                                        style={
                                                            "background-color": "#4CAF50", 
                                                            "color": "white", 
                                                            "font-size": "14px",
                                                            "font-weight": "bold",
                                                            "border-radius": "5px",
                                                            "padding": "5px 40px", 
                                                            "margin-top": "40px", 
                                                            "border": "none", 
                                                            "cursor": "pointer"
                                                        }
                                                    ),
                                                ],
                                                style={
                                                    "margin-top": "50px", 
                                                    "text-align": "right",  # Align the buttons to the right
                                                    "width": "100%",  # Ensure it spans the full width of the container
                                                },
                                            ),
                                        ],
                                        style={
                                            "padding-top": "20px", 
                                            "padding-left": "50px", 
                                            "padding-bottom": "20px", 
                                            "padding-right": "20px",  
                                            "text-align": "left", 
                                            "background-color": "#f9f9f9", 
                                            "display": "flex",  # Set display to flex
                                            "flex-direction": "row",  # Align labels and input fields in a row (inline)
                                            "gap": "20px",  # Space between the two input sections
                                        },
                                    )
                                ],
                            ),

 
                            ],
                        ),
                    ],
                ),
            ],
        ),
            html.Div(id='save-status-medical-record'),
    ]
)

def edit_mode_medical_record(app):
    # Callback to fetch and store doctor data in the store component
    @app.callback(
        Output('medical-record-data-store', 'data'),
        Input("url", "search")  # Listening to changes in URL (assuming patient_id is part of the query)
    )
    def fetch_and_store_data(search):
        start_time = time.time()  # Start timing the execution

        medical_record_data = None
        if search:
            query_params = parse_qs(search[1:])  # Remove leading '?' and parse the query string
            patient_id = query_params.get('patient_id', [None])[0]  # Get the patient_id from the query parameters
            if patient_id:
                medical_record_data = fetch_service_details(patient_id)

        if medical_record_data:
            return {
                'patient_first_name': medical_record_data.get('patient_first_name', ''),
                'patient_last_name': medical_record_data.get('patient_last_name', ''),
            }
        else:
            return {'patient_first_name': '', 'patient_last_name': ''}

    # Callback to update input fields with data from the store component
    @app.callback(
        [
            Output('first-name-type-input-edit-mode', 'value'),
            Output('last-name-input-edit-mode', 'value'),
        ],
        Input('medical-record-data-store', 'data')
    )
    def update_input_fields(medical_record_data):
        if medical_record_data:
            print(f"Updating input fields with patient data: {medical_record_data}")
            return (
                medical_record_data.get('patient_first_name', ''),
                medical_record_data.get('patient_last_name', ''),
            )
        return '', ''

    # Callback to save updated data to the database
    @app.callback(
        Output('save-status-medical-record', 'children'),  # A status message to confirm save
        Input('save-button', 'n_clicks'),  # Trigger on button click
        [
            State('url', 'search'),  # Get patient ID from the URL
            State('first-name-type-input-edit-mode', 'value'),
            State('last-name-input-edit-mode', 'value'),
        ],
        prevent_initial_call=True  # Only trigger when button is clicked
    )
    def save_data(n_clicks, search, first_name, last_name):
        if not search:
            return "Error: No patient ID found in the URL."

        query_params = parse_qs(search[1:])  # Parse query string
        patient_id = query_params.get('patient_id', [None])[0]
        if not patient_id:
            return "Error: No valid patient ID found."

        try:
            update_patient_details(patient_id, first_name, last_name)
            return "Success: Patient data saved successfully."
        except Exception as e:
            print(f"Error saving data: {e}")
            return "Error: Failed to save patient data."
        