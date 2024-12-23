import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Output, Input
from dash.exceptions import PreventUpdate
from apps.dbconnect import create_connection, close_connection
from urllib.parse import parse_qs
import time

# Function to fetch service details from the database
def fetch_service_details(patient_id):
    connection = create_connection()
    data = None
    if connection: 
        cursor = connection.cursor()
        query = """
        SELECT patient_first_name, patient_last_name, patient_birthday, patient_age, patient_sex, 
        patient_contact_number, patient_civil_status, patient_occupation, patient_address
        FROM patient
        WHERE patient_id = %s
        """
        print(f"Executing query for patient_id: {patient_id}")  # Debugging line
        cursor.execute(query, (patient_id,))
        data = cursor.fetchone()
        print(f"Query result: {data}")  # Debugging line
        close_connection(connection)
    else:
        print("Database connection failed.")  # Debugging line
    return data

# Define styles for the layout
styles = {
    "subHeader1": {
        "padding": "40px",
        "marginLeft": "60px"
    },
    "backPatientInfo": {
        "fontSize": "18px", 
        "color": "#05066d",
        "marginTop": "-30px"
    },
    "patientInfo": {
        "fontSize": "30px",
        "color": "#05066d",
        "marginTop": "-5px"
    },
    "divider1": {
        "marginTop": "-3px",
        "width": "93%",
        "border": "2px solid #05066d"
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
                                "Back to Patient Information Page"
                            ],
                            href="/patient_information",  # Link target
                            style={
                                **styles["backPatientInfo"],  # Apply existing styles
                                "text-decoration": "none",  # Remove underline
                                "color": "inherit"  # Ensure link text inherits color from parent
                            },
                        ),
                    ],
                    style={"margin-bottom": "50px"},
                ),
                html.H2("Patient Information", style=styles["patientInfo"]),
                html.Hr(style=styles["divider1"]),
            ],
        ),  

    # The table - View Patient Information/Record
    html.Div(
    style={"padding": "0px"},
    children=[
        html.Div(
            style={"padding": "10px"},
            children=[
                # Table Container with smaller width
                html.Table(
                    style={
                        "width": "85%",  # Table width
                        "margin-left": "90px",  # Move the table to the left
                        "margin-top": "-50px",  
                        "border": "1px solid black", 
                        "border-collapse": "collapse", 
                    },
                    children=[
                        # Table Header Row
                        html.Tr(
                            children=[
                                html.Th(
                                    children=[
                                        "View Patient Record",
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
                                        # Wrapper for flex layout
                                        html.Div(
                                            children=[
                                                # Patient First Name
                                                html.Div(
                                                    children=[
                                                        "Patient First Name",
                                                        html.Br(),  # Line break
                                                        dcc.Input(
                                                            id="first-name-input-view",  # ID for the input field
                                                            type="text",  # Type of the input field (text)
                                                            placeholder="Juan",  # Placeholder text for the input
                                                            style={"width": "300px", "padding": "5px", "margin-bottom": "15px", "font-style": "italic"}  # Input style
                                                        ),
                                                    ],
                                                    style={"margin-right": "20px", "text-align": "left"},  # Spacing and alignment
                                                ),
                                                # Patient Last Name
                                                html.Div(
                                                    children=[
                                                        "Patient Last Name",
                                                        html.Br(),  # Line break
                                                        dcc.Input(
                                                            id="last-name-input-view",  # ID for the input field
                                                            type="text",  # Type of the input field (text)
                                                            placeholder="Dela Cruz",  # Placeholder text for the input
                                                            style={"width": "300px", "padding": "5px", "margin-bottom": "15px", "font-style": "italic"}  # Input style
                                                        ),
                                                    ],
                                                    style={"text-align": "left"},  # Alignment
                                                ),
                                            ],
                                            style={
                                                "display": "flex",  # Flex layout for inline positioning
                                                "gap": "20px",  # Space between elements
                                            },
                                        ),

                                        # Second line input fields
                                        html.Div(
                                            children=[
                                                # Patient Birthday
                                                html.Div(
                                                    children=[
                                                        "Birthday",
                                                        html.Br(),  # Line break
                                                        dcc.DatePickerSingle(
                                                            id="date-picker-bday-view",
                                                            placeholder="mm/dd/yyyy",  # Placeholder format
                                                            display_format="MM/DD/YYYY",  # Display format
                                                            style={
                                                                "margin-right": "115px",
                                                                "margin-bottom": "15px",  # Adjusted margin for bottom spacing
                                                                "width": "100px",  # Set width to 100px
                                                            },
                                                            className="custom-date-picker"  # Add a custom class for specific targeting
                                                        ),
                                                    ],
                                                    style={"margin-right": "20px", "text-align": "left"},  # Spacing and alignment
                                                ),

                                                # Patient age
                                                html.Div(
                                                    children=[
                                                        "Age",
                                                        html.Br(),  # Line break
                                                        dcc.Input(
                                                            id="age-input-view",  # ID for the input field
                                                            type="number",  # Type of the input field (text)
                                                            placeholder="20",  # Placeholder text for the input
                                                            style={"width": "80px", "padding": "5px", "margin-bottom": "15px", "margin-right": "15px", "font-style": "italic"}  # Input style
                                                        ),
                                                    ],
                                                    style={"text-align": "left"},  # Alignment
                                                ),

                                                  # Patient sex/gender
                                                    html.Div(
                                                        children=[
                                                            "Sex",
                                                            html.Br(),  # Line break
                                                            dcc.Dropdown(
                                                                id="gender-dropdown-view",  # ID for the dropdown
                                                                options=[
                                                                    {"label": "Female", "value": "Female"},
                                                                    {"label": "Male", "value": "Male"},
                                                                    {"label": "Others", "value": "Others"}
                                                                ],
                                                                placeholder="Select Gender",  # Placeholder text
                                                                style={
                                                                    "width": "200px", 
                                                                    "height": "40px", 
                                                                    "padding": "2px", 
                                                                    "font-style": "italic",
                                                                    "margin-bottom": "15px",
                                                                    "margin-right": "15px",
                                                                }  # Dropdown style
                                                            ),

                                                        ],
                                                        style={"text-align": "left"},  # Alignment
                                                    ),

                                                    # Patient contact number
                                                    html.Div(
                                                        children=[
                                                            "Contact Number",
                                                            html.Br(),  # Line break
                                                            dcc.Input(
                                                                id="contact-input-view",  # ID for the input field
                                                                type="number",  # Type of the input field (text)
                                                                placeholder="0927 123 4567",  # Placeholder text for the input
                                                                style={"width": "300px", "padding": "5px", "margin-bottom": "15px", "font-style": "italic"}  # Input style
                                                            ),
                                                        ],
                                                        style={"text-align": "left"},  # Alignment
                                                    ),
                                            ],
                                            style={
                                                "display": "flex",  # Flex layout for inline positioning
                                                "gap": "20px",  # Space between elements
                                            },
                                        ),

                                        # Third line input fields
                                        html.Div(
                                            children=[
                                                # Patient Civil Status
                                                html.Div(
                                                    children=[
                                                        "Civil Status",
                                                        html.Br(),  # Line break
                                                        dcc.Input(
                                                            id="civil-status-input-view",  # ID for the input field
                                                            type="text",  # Type of the input field (text)
                                                            placeholder="Single",  # Placeholder text for the input
                                                            style={"width": "200px", "padding": "5px", "margin-right": "15px", "font-style": "italic"}  # Input style
                                                        ),
                                                    ],
                                                    style={"margin-right": "20px", "text-align": "left"},  # Spacing and alignment
                                                ),
                                                # Patient Occupation
                                                html.Div(
                                                    children=[
                                                        "Occupation",
                                                        html.Br(),  # Line break
                                                        dcc.Input(
                                                            id="occupation-input-view",  # ID for the input field
                                                            type="text",  # Type of the input field (text)
                                                            placeholder="student",  # Placeholder text for the input
                                                            style={"width": "200px", "padding": "5px", "margin-right": "30px", "font-style": "italic"}  # Input style
                                                        ),
                                                    ],
                                                    style={"text-align": "left"},  # Alignment
                                                ),

                                                    # Patient contact number
                                                    html.Div(
                                                        children=[
                                                            "Address",
                                                            html.Br(),  # Line break
                                                            dcc.Input(
                                                                id="address-input-view",  # ID for the input field
                                                                type="text",  # Type of the input field (text)
                                                                placeholder="123 Roxas Ave, Diliman, Quezon City",  # Placeholder text for the input
                                                                style={"width": "400px", "padding": "5px", "font-style": "italic"}  # Input style
                                                            ),
                                                        ],
                                                        style={"text-align": "left", "margin-bottom": "40px"},  # Alignment
                                                    ),
                                            ],
                                            style={
                                                "display": "flex",  # Flex layout for inline positioning
                                                "gap": "20px",  # Space between elements
                                            },
                                        ),
                                    ],
                                    style={
                                        "padding-top": "30px", 
                                        "padding-left": "50px", 
                                        "padding-bottom": "20px", 
                                        "padding-right": "20px", 
                                        "text-align": "left", 
                                        "background-color": "#f9f9f9", 
                                        "font-weight": "bold", 
                                        "color": "#05066d",
                                        "margin": "15px"  # Added margin to the table cell for spacing around the content
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
    ]
)

def view_patient_info_mode(app):
    # Callback to fetch and store patient data in the store component
    @app.callback(
        Output('view-patient-info-data-store', 'data'),
        Input("url", "search")  # Listening to changes in URL (assuming patient_id is part of the query)
    )
    def fetch_and_store_data(search):
        start_time = time.time()  # Start timing the execution

        patient_info_view_data = None
        if search:
            query_params = parse_qs(search[1:])  # Remove leading '?' and parse the query string
            patient_id = query_params.get('patient_id', [None])[0]  # Get the patient_id
            if patient_id:
                patient_info_view_data = fetch_service_details(patient_id)

        end_time = time.time()  # End timing the execution
        print(f"Callback execution time: {end_time - start_time} seconds")  # Debugging line

        # Map the fetched patient details into the data structure to store in the component
        if patient_info_view_data:
            return {
                'patient_first_name': patient_info_view_data[0],
                'patient_last_name': patient_info_view_data[1],
                'patient_birthday': patient_info_view_data[2],
                'patient_age': patient_info_view_data[3],
                'patient_sex': patient_info_view_data[4],
                'patient_contact_number': patient_info_view_data[5],
                'patient_civil_status': patient_info_view_data[6],
                'patient_occupation': patient_info_view_data[7],
                'patient_address': patient_info_view_data[8]
            }
        else:
            return {  # Default to empty if no data is available
                'patient_first_name': '',
                'patient_last_name': '',
                'patient_birthday': '',
                'patient_age': '',
                'patient_sex': '',
                'patient_contact_number': '',
                'patient_civil_status': '',
                'patient_occupation': '',
                'patient_address': ''
            }

    # Callback to update input fields with data from store component
    @app.callback(
        [
            Output('first-name-input-view', 'value'),
            Output('last-name-input-view', 'value'),
            Output('date-picker-bday-view', 'date'),
            Output('age-input-view', 'value'),
            Output('gender-dropdown-view', 'value'),
            Output('contact-input-view', 'value'),
            Output('civil-status-input-view', 'value'),
            Output('occupation-input-view', 'value'),
            Output('address-input-view', 'value'),
        ],
        Input('view-patient-info-data-store', 'data')
    )
    def update_input_fields(patient_info_view_data):
        if patient_info_view_data:
            print(f"Updating input fields with patient data: {patient_info_view_data}")  # Debugging line
            return (
                patient_info_view_data.get('patient_first_name', ''),
                patient_info_view_data.get('patient_last_name', ''),
                patient_info_view_data.get('patient_birthday', ''),
                patient_info_view_data.get('patient_age', ''),
                patient_info_view_data.get('patient_sex', ''),
                patient_info_view_data.get('patient_contact_number', ''),
                patient_info_view_data.get('patient_civil_status', ''),
                patient_info_view_data.get('patient_occupation', ''),
                patient_info_view_data.get('patient_address', '')
            )
        return ('', '', '', '', '', '', '', '', '')  # Default to empty if no data is available