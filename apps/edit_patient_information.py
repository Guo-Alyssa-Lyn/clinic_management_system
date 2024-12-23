import dash_bootstrap_components as dbc
from dash import dcc, html, Output, Input, State
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
        SELECT patient_first_name, patient_last_name, patient_birthday, patient_age,
        patient_sex, patient_contact_number, patient_civil_status, patient_occupation, patient_address
        FROM patient
        WHERE patient_id = %s
        """
        print(f"Executing query for service_id: {patient_id}")  # Debugging line
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
        "marginTop": "-30px",
        "color": "#05066d"
    },
    "patientInfo": {
        "fontSize": "30px",
        "color": "#05066d"
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

# The table - Edit New Patient
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
                                        "Edit Patient Information",
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
                                                            id="first-name-input-edit",  # ID for the input field
                                                            type="text",  # Type of the input field (text)
                                                            placeholder="Juan",  # Placeholder text for the input
                                                            style={"width": "250px", "padding": "5px", "margin-bottom": "10px", "font-style": "italic"}  # Input style
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
                                                            id="last-name-input-edit",  # ID for the input field
                                                            type="text",  # Type of the input field (text)
                                                            placeholder="Dela Cruz",  # Placeholder text for the input
                                                            style={"width": "250px", "padding": "5px", "font-style": "italic"}  # Input style
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
                                                # Patient Date of Visit
                                                html.Div(
                                                    children=[
                                                        "Birthday",
                                                        html.Br(),  # Line break
                                                        dcc.DatePickerSingle(
                                                            id="birthday-picker-edit",
                                                            placeholder="mm/dd/yyyy",  # Placeholder format
                                                            display_format="MM/DD/YYYY",  # Display format
                                                            style={
                                                                "margin-right": "150px",
                                                                "margin-bottom": "10px",  # Adjusted margin for bottom spacing
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
                                                            id="age-input-edit",  # ID for the input field
                                                            type="number",  # Type of the input field (text)
                                                            placeholder="20",  # Placeholder text for the input
                                                            style={"width": "50px", "padding": "5px", "margin-right": "20px", "font-style": "italic"}  # Input style
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
                                                                id="gender-dropdown-edit",  # ID for the dropdown
                                                                options=[
                                                                    {"label": "Female", "value": "Female"},
                                                                    {"label": "Male", "value": "Male"},
                                                                    {"label": "Others", "value": "Others"}
                                                                ],
                                                                placeholder="Select Gender",  # Placeholder text
                                                                style={
                                                                    "width": "250px", 
                                                                    "padding": "2px", 
                                                                    "margin-right": "20px", 
                                                                    "font-style": "italic"
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
                                                                id="contact-input-edit",  # ID for the input field
                                                                type="number",  # Type of the input field (text)
                                                                placeholder="0927 123 4567",  # Placeholder text for the input
                                                                style={"width": "250px", "padding": "5px", "font-style": "italic"}  # Input style
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
                                                            id="civil-status-input-edit",  # ID for the input field
                                                            type="text",  # Type of the input field (text)
                                                            placeholder="Single",  # Placeholder text for the input
                                                            style={"width": "250px", "padding": "5px", "margin-bottom": "50px", "font-style": "italic"}  # Input style
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
                                                            id="occupation-input-edit",  # ID for the input field
                                                            type="text",  # Type of the input field (text)
                                                            placeholder="student",  # Placeholder text for the input
                                                            style={"width": "250px", "padding": "5px", "margin-right": "20px", "font-style": "italic"}  # Input style
                                                        ),
                                                    ],
                                                    style={"text-align": "left"},  # Alignment
                                                ),

                                                    # Patient address
                                                    html.Div(
                                                        children=[
                                                            "Address",
                                                            html.Br(),  # Line break
                                                            dcc.Input(
                                                                id="address-input-edit",  # ID for the input field
                                                                type="text",  # Type of the input field (text)
                                                                placeholder="123 Roxas Ave, Diliman, Quezon City",  # Placeholder text for the input
                                                                style={"width": "345px", "padding": "5px", "font-style": "italic"}  # Input style
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
                                                            "font-weight": "bold",
                                                            "font-size": "14px",
                                                            "padding": "5px 40px", 
                                                            "border-radius": "5px",
                                                            "margin-top": "40px", 
                                                            "margin-right": "20px", 
                                                            "border": "none", 
                                                            "cursor": "pointer"
                                                        }
                                                    ),
                                                    href="/patient_information",  # Replace with the desired link
                                                ),
                                                html.Button(
                                                    "Save", 
                                                    id="save-button",
                                                    n_clicks=0,
                                                    style={
                                                        "background-color": "#4CAF50", 
                                                        "color": "white", 
                                                        "font-weight": "bold",
                                                        "font-size": "14px",
                                                        "border-radius": "5px",
                                                        "padding": "5px 40px", 
                                                        "margin-top": "40px", 
                                                        "border": "none", 
                                                        "cursor": "pointer"
                                                    }
                                                ),
                                            ],
                                            style={
                                                "margin-top": "10px", 
                                                "text-align": "right",  # Align the buttons to the right
                                                "width": "100%",  # Ensure it spans the full width of the container
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
        html.Div(id="save-status-patient-info", children="")
    ]
)

def edit_mode_info(app):
    # Callback to fetch and store patient data in the store component
    @app.callback(
        Output('patient-data-store', 'data'),
        Input("url", "search")  # Listening to changes in URL (assuming patient_id is part of the query)
    )
    def fetch_and_store_data(search):
        start_time = time.time()  # Start timing the execution

        patient_data = None
        if search:
            query_params = parse_qs(search[1:])  # Remove leading '?' and parse the query string
            patient_id = query_params.get('patient_id', [None])[0]  # Get the patient_id
            if patient_id:
                patient_data = fetch_service_details(patient_id)

        end_time = time.time()  # End timing the execution
        print(f"Callback execution time: {end_time - start_time} seconds")  # Debugging line

        if patient_data:
            return {
                'patient_first_name': patient_data[0],
                'patient_last_name': patient_data[1],
                'patient_birthday': patient_data[2],
                'patient_age': patient_data[3],
                'patient_sex': patient_data[4],
                'patient_contact_number': patient_data[5],
                'patient_civil_status': patient_data[6],
                'patient_occupation': patient_data[7],
                'patient_address': patient_data[8],
            }
        else:
            # Default empty values if no data is found
            return {
                'patient_first_name': '',
                'patient_last_name': '',
                'patient_birthday': '',
                'patient_age': '',
                'patient_sex': '',
                'patient_contact_number': '',
                'patient_civil_status': '',
                'patient_occupation': '',
                'patient_address': '',
            }

    # Callback to update input fields with data from the store component
    @app.callback(
        [
            Output('first-name-input-edit', 'value'),
            Output('last-name-input-edit', 'value'),
            Output('birthday-picker-edit', 'date'),
            Output('age-input-edit', 'value'),
            Output('gender-dropdown-edit', 'value'),
            Output('contact-input-edit', 'value'),
            Output('civil-status-input-edit', 'value'),
            Output('occupation-input-edit', 'value'),
            Output('address-input-edit', 'value'),
        ],
        Input('patient-data-store', 'data')
    )
    def update_input_fields(patient_data):
        if patient_data:
            print(f"Updating input fields with patient data: {patient_data}")  # Debugging line
            return (
                patient_data.get('patient_first_name', ''),
                patient_data.get('patient_last_name', ''),
                patient_data.get('patient_birthday', ''),
                patient_data.get('patient_age', ''),
                patient_data.get('patient_sex', ''),
                patient_data.get('patient_contact_number', ''),
                patient_data.get('patient_civil_status', ''),
                patient_data.get('patient_occupation', ''),
                patient_data.get('patient_address', '')
            )
        # Default empty values for all fields if no data is available
        return '', '', '', '', '', '', '', '', ''

    # Callback to save the updated patient data into the database
    @app.callback(
        Output('save-status-patient-info', 'children'),  # A component to display save status
        Input('save-button', 'n_clicks'),   # Triggered when save button is clicked
        State('first-name-input-edit', 'value'),
        State('last-name-input-edit', 'value'),
        State('birthday-picker-edit', 'date'),
        State('age-input-edit', 'value'),
        State('gender-dropdown-edit', 'value'),
        State('contact-input-edit', 'value'),
        State('civil-status-input-edit', 'value'),
        State('occupation-input-edit', 'value'),
        State('address-input-edit', 'value'),
        State("url", "search"),  # To retrieve patient_id from the URL
        prevent_initial_call=True  # Prevents the callback from firing on page load
    )
    def save_patient_data(n_clicks, first_name, last_name, birthday, age, sex,
                          contact_number, civil_status, occupation, address, search):
        if not search:
            return "Failed: Missing patient ID from URL."
        
        # Parse patient ID from the URL
        query_params = parse_qs(search[1:])
        patient_id = query_params.get('patient_id', [None])[0]
        
        if not patient_id:
            return "Failed: Invalid patient ID."

        # Prepare and execute the database update
        connection = create_connection()
        if connection:
            try:
                cursor = connection.cursor()
                update_query = """
                UPDATE patient
                SET 
                    patient_first_name = %s,
                    patient_last_name = %s,
                    patient_birthday = %s,
                    patient_age = %s,
                    patient_sex = %s,
                    patient_contact_number = %s,
                    patient_civil_status = %s,
                    patient_occupation = %s,
                    patient_address = %s
                WHERE patient_id = %s
                """
                cursor.execute(update_query, (
                    first_name, last_name, birthday, age, sex,
                    contact_number, civil_status, occupation, address, patient_id
                ))
                connection.commit()
                return "Patient data successfully updated."
            except Exception as e:
                print(f"Error updating patient data: {e}")
                return f"Failed to update patient data: {str(e)}"
            finally:
                close_connection(connection)
        else:
            return "Database connection failed. Please try again."