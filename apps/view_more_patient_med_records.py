import dash_bootstrap_components as dbc
from dash import dcc, html, Output, Input
from dash.exceptions import PreventUpdate
from apps.dbconnect import create_connection, close_connection
from urllib.parse import parse_qs
import time

# Function to fetch details from the database
def fetch_service_details(patient_id):
    connection = create_connection()
    data = None
    if connection:
        cursor = connection.cursor()
        query = """
        SELECT 
            p.patient_height, p.patient_weight,
            m.record_bloodpressure, m.record_temperature, m.record_consultation_type,
            m.record_diagnosis, m.record_treatment, m.record_lab_result, m.record_side_note,
            a.appointment_date
        FROM patient p
        JOIN medical_record m ON p.patient_id = m.patient_id
        JOIN appointment a ON p.patient_id = a.patient_id
        WHERE p.patient_id = %s
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
    "backViewMedicalRecords": {
        "marginTop": "-30px",
        "fontSize": "18px",
        "color": "#05066d",
    },
    "titlePatientInfo": {
        "fontSize": "30px",
        "color": "#05066d",
        "fontWeight": "bold",
    },
    "divider1": {
        "width": "93%",
        "border": "2px solid #05066d",
        "marginTop": "-3px"
    },
    "patientRecords": {
        "fontSize": "18px",
        "color": "#05066d",
    },
    "patientName": {
        "fontSize": "18px",
        "color": "#05066d",
        "fontWeight": "bold"
    }
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
                                "Back to View Patient Medical Records Page"
                            ],
                            href="/view_patient_medical_records",  # Link target 
                            style={
                                **styles["backViewMedicalRecords"],  # Apply existing styles
                                "text-decoration": "none",  # Remove underline
                                "color": "inherit"  # Ensure link text inherits color from parent
                            },
                        ),
                    ],
                    style={"margin-bottom": "50px"}, 
                ),
                html.H2("Patient Information", style=styles["titlePatientInfo"]),
                html.Hr(style=styles["divider1"]),
                html.H3(
                            id='patient-name',  # Dynamically updated patient name
                            style={
                                'marginBottom': '20px',
                                'fontSize': '20px',
                                'color': '#05066d',
                                'fontWeight': 'bold',
                            }
                        ),
            ],
        ),

        # Window - View Patient Medical Record - To View More Info
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
                                        "View Patient Medical Record",
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
                                                # Height 
                                                html.Div(
                                                    children=[
                                                        "Height (in cm)",
                                                        html.Br(),  # Line break
                                                        dcc.Input(
                                                            id="height-input-view",  # ID for the input field
                                                            type="number",  # Type of the input field (text)
                                                            placeholder="160",  # Placeholder text for the input
                                                            style={"width": "100px", "padding": "5px", "margin-bottom": "50px", "margin-right": "50px", "font-style": "italic"}  # Input style
                                                        ),
                                                    ],
                                                    style={"margin-right": "20px", "text-align": "left"},  # Spacing and alignment
                                                ),
                                                # Weight
                                                html.Div(
                                                    children=[
                                                        "Weight (in kg)",
                                                        html.Br(),  # Line break
                                                        dcc.Input(
                                                            id="weight-input-view",  # ID for the input field
                                                            type="number",  # Type of the input field (text)
                                                            placeholder="160",  # Placeholder text for the input
                                                            style={"width": "100px", "padding": "5px", "margin-right": "50px", "font-style": "italic"}  # Input style
                                                        ),
                                                    ],
                                                    style={"text-align": "left"},  # Alignment
                                                ),
                                                # Blood Pressure
                                                html.Div(
                                                    children=[
                                                        "Blood Pressure",
                                                        html.Br(),  # Line break
                                                        dcc.Input(
                                                            id="blood-pressure-input-view",  # ID for the input field
                                                            type="text",  # Type of the input field (text)
                                                            placeholder="120/80",  # Placeholder text for the input
                                                            style={"width": "100px", "padding": "5px", "margin-right": "50px", "font-style": "italic"}  # Input style
                                                        ),
                                                    ],
                                                    style={"text-align": "left"},  # Alignment
                                                ),
                                                 # Temperature
                                                html.Div(
                                                    children=[
                                                        "Temperature (in °C)",
                                                        html.Br(),  # Line break
                                                        dcc.Input(
                                                            id="temp-input-view",  # ID for the input field
                                                            type="number",  # Type of the input field (text)
                                                            placeholder="38",  # Placeholder text for the input
                                                            style={"width": "100px", "padding": "5px", "margin-right": "50px", "font-style": "italic"}  # Input style
                                                        ),
                                                    ],
                                                    style={"text-align": "left"},  # Alignment
                                                ),
                                            ],
                                            style={
                                                "display": "flex",  # Flex layout for inline positioning
                                                "gap": "20px",  # Space between elements
                                                "margin-bottom": "10px",
                                            },
                                        ),

                                        # Second line input fields
                                        html.Div(
                                            children=[
                                                # Date of Visit
                                                  html.Div(
                                                    children=[
                                                        "Date of Visit",
                                                        html.Br(),  # Line break
                                                        dcc.DatePickerSingle(
                                                            id="date-appointment-view",
                                                            placeholder="mm/dd/yyyy",  # Placeholder format
                                                            display_format="MM/DD/YYYY",  # Display format
                                                            style={
                                                                "margin-right": "168px",
                                                                "margin-bottom": "15px",  # Adjusted margin for bottom spacing
                                                                "width": "100px",  # Set width to 100px
                                                            },
                                                            className="custom-date-picker"  # Add a custom class for specific targeting
                                                        ),
                                                    ],
                                                    style={"margin-right": "30px", "text-align": "left"},  # Spacing and alignment
                                                ),
                                                # Consultation Type
                                                html.Div(
                                                    children=[
                                                        "Consultation Type",
                                                        html.Br(),  # Line break
                                                        dcc.Input(
                                                            id="consult-type-input-view",  # ID for the input field
                                                            type="text",  # Type of the input field (text)
                                                            placeholder="Lorem ipsum",  # Placeholder text for the input
                                                            style={"width": "250px", "padding": "5px", "margin-right": "30px", "font-style": "italic"}  # Input style
                                                        ),
                                                    ],
                                                    style={"text-align": "left"},  # Alignment
                                                ),

                                                  # Diagnosis
                                                    html.Div(
                                                        children=[
                                                            "Diagnosis",
                                                            html.Br(),  # Line break
                                                            dcc.Input(
                                                                id="diagnosis-input-view",  # ID for the input field
                                                                type="text",  # Type of the input field (text)
                                                                placeholder="Lorem ipsum",  # Placeholder text for the input
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
                                                # Treatment
                                                html.Div(
                                                    children=[
                                                        "Treatment",
                                                        html.Br(),  # Line break
                                                            dcc.Input(
                                                                id="treatment-input-view",  # ID for the input field
                                                                type="text",  # Type of the input field (text)
                                                                placeholder="Lorem ipsum",  # Placeholder text for the input
                                                                style={"width": "250px", "margin-right": "28px", "padding": "5px", "font-style": "italic"}  # Input style
                                                            ),
                                                    ],
                                                    style={"margin-right": "20px", "text-align": "left"},  # Spacing and alignment
                                                ),
                                                # Lab Result
                                                html.Div(
                                                    children=[
                                                        "Lab Result",
                                                        html.Br(),  # Line break
                                                        dcc.Input(
                                                            id="lab-res-input-view",  # ID for the input field
                                                            type="text",  # Type of the input field (text)
                                                            placeholder="Lorem ipsum",  # Placeholder text for the input
                                                            style={"width": "250px", "padding": "5px", "margin-right": "30px", "font-style": "italic"}  # Input style
                                                        ),
                                                    ],
                                                    style={"text-align": "left"},  # Alignment
                                                ),

                                                    # Side Note
                                                    html.Div(
                                                        children=[
                                                            "Side Note",
                                                            html.Br(),  # Line break
                                                            dcc.Input(
                                                                id="note-input-view",  # ID for the input field
                                                                type="text",  # Type of the input field (text)
                                                                placeholder="Lorem ipsum",  # Placeholder text for the input
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

                                    
                                    ],
                                    style={
                                        "padding-top": "30px", 
                                        "padding-left": "50px", 
                                        "padding-bottom": "60px", 
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

def view_mode_medical_records(app):
    # Callback to fetch and store patient data in the store component
    @app.callback(
        Output('view-patient-medical-records-data-store', 'data'),
        Input("url", "pathname")  # Listen to changes in the URL path (not the query string)
    )
    def fetch_and_store_data(pathname):
        start_time = time.time()  # Start timing the execution

        patient_medical_record_view_data = None

        # Debugging the URL and pathname
        print(f"Received URL pathname: {pathname}")  # Debugging line

        if pathname:
            # Extract patient_id from the pathname (e.g., '/view_medical_records_history/1')
            patient_id = pathname.split('/')[-1]  # Get the last part of the path
            print(f"Extracted patient_id: {patient_id}")  # Debugging line

            if patient_id:
                patient_medical_record_view_data = fetch_service_details(patient_id)
                print(f"Fetched data from database: {patient_medical_record_view_data}")  # Debugging line
            else:
                print("No patient_id found in the URL.")  # Debugging line

        end_time = time.time()  # End timing the execution
        print(f"Callback execution time: {end_time - start_time} seconds")  # Debugging line

        # Map the fetched patient details into the data structure to store in the component
        if patient_medical_record_view_data:
            print(f"Returning data to store component: {patient_medical_record_view_data}")  # Debugging line
            return {
                'patient_height': patient_medical_record_view_data[0],
                'patient_weight': patient_medical_record_view_data[1],
                'record_bloodpressure': patient_medical_record_view_data[2],
                'record_temperature': patient_medical_record_view_data[3],
                'record_consultation_type': patient_medical_record_view_data[4],
                'record_diagnosis': patient_medical_record_view_data[5],
                'record_treatment': patient_medical_record_view_data[6],
                'record_lab_result': patient_medical_record_view_data[7],
                'record_side_note': patient_medical_record_view_data[8],
                'appointment_date': patient_medical_record_view_data[9]
            }
        else:
            print("No data fetched from the database.")  # Debugging line
            return {  # Default to empty if no data is available
                'patient_height': '',
                'patient_weight': '',
                'record_bloodpressure': '',
                'record_temperature': '',
                'record_consultation_type': '',
                'record_diagnosis': '',
                'record_treatment': '',
                'record_lab_result': '',
                'record_side_note': '',
                'appointment_date': '',
            }

    # Callback to update input fields with data from store component
    @app.callback(
        [
            Output('height-input-view', 'value'),
            Output('weight-input-view', 'value'),
            Output('blood-pressure-input-view', 'value'),
            Output('temp-input-view', 'value'),
            Output('date-appointment-view', 'date'),
            Output('consult-type-input-view', 'value'),
            Output('diagnosis-input-view', 'value'),
            Output('treatment-input-view', 'value'),
            Output('lab-res-input-view', 'value'),
            Output('note-input-view', 'value'),
        ],
        Input('view-patient-medical-records-data-store', 'data')
    )
    def update_input_fields(patient_medical_record_view_data):
        if patient_medical_record_view_data:
            print(f"Updating input fields with patient data: {patient_medical_record_view_data}")  # Debugging line
            return (
                patient_medical_record_view_data.get('patient_height', ''),
                patient_medical_record_view_data.get('patient_weight', ''),
                patient_medical_record_view_data.get('record_bloodpressure', ''),
                patient_medical_record_view_data.get('record_temperature', ''),
                patient_medical_record_view_data.get('appointment_date', ''),
                patient_medical_record_view_data.get('record_consultation_type', ''),
                patient_medical_record_view_data.get('record_diagnosis', ''),
                patient_medical_record_view_data.get('record_treatment', ''),
                patient_medical_record_view_data.get('record_lab_result', ''),
                patient_medical_record_view_data.get('record_side_note', '')
            )
        return ('', '', '', '', '', '', '', '', '', '')  # Default to empty if no data is available