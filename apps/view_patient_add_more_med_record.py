import dash_bootstrap_components as dbc
from dash import dcc, html, Output, Input, State
from dash.exceptions import PreventUpdate
import logging
from apps.dbconnect import create_connection, close_connection
import datetime

logging.basicConfig(level=logging.DEBUG)

# Define styles for the layout
styles = {
    "subHeader1": {
        "padding": "40px",
        "marginLeft": "60px"
    },
    "backViewMedicalRecords": {
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
                                "vertical-align": "middle"  # Adjust size and alignment
                            },
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
            style={"margin-bottom": "50px"},  # Bottom margin for spacing
        ),
        
        # Title and Divider
        html.H2("Patient Information", style={"font-size": "24px", "font-weight": "bold"}),
        html.Hr(style=styles["divider1"]),  # Divider line

        # Patient's name dynamically displayed
        html.H3(
            id='patient-name',  # Dynamically updated patient name
            style={
                'marginTop': '0px',
                'marginBottom': '20px',
                'fontSize': '20px',
                'color': '#05066d',
                'fontWeight': 'bold',
            }
        ),
    ],
),
    # Window - View Patient Medical Record - To Add More Info
    html.Div(
    style={"padding": "0px"},
    children=[
        # Hidden input to store the patient_id (can be dynamically set or passed as a session variable)
        dcc.Input(id="patient-id", type="hidden", value="123"),  # Replace with dynamic logic for patient ID

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
                                        "Add Patient Medical Record",
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
                                                            id="height-input-add",  # ID for the input field
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
                                                            id="weight-input-add",  # ID for the input field
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
                                                            id="blood-pressure-input-add",  # ID for the input field
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
                                                            id="temp-input-add",  # ID for the input field
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
                                                            id="date-picker-visit-add-auto",
                                                            placeholder="YYYY-MM-DD",  # Placeholder format
                                                            display_format="YYYY-MM-DD",  # Display format
                                                            style={
                                                                "margin-right": "168px",
                                                                "margin-bottom": "15px",  # Adjusted margin for bottom spacing
                                                                "width": "100px",  # Set width to 100px
                                                            },
                                                            className="custom-date-picker"  # Add a custom class for specific targeting
                                                        ),
                                                    ],
                                                    style={"margin-right": "20px", "text-align": "left"},  # Spacing and alignment
                                                ),
                                                # Consultation Type
                                                html.Div(
                                                    children=[
                                                        "Consultation Type",
                                                        html.Br(),  # Line break
                                                        dcc.Input(
                                                            id="consult-type-input-add",  # ID for the input field
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
                                                                id="diagnosis-input-add",  # ID for the input field
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
                                                                id="treatment-input-add",  # ID for the input field
                                                                type="text",  # Type of the input field (text)
                                                                placeholder="Lorem ipsum",  # Placeholder text for the input
                                                                style={"width": "250px", "margin-right": "20px", "padding": "5px", "font-style": "italic"}  # Input style
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
                                                            id="lab-res-input-add",  # ID for the input field
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
                                                                id="note-input-add",  # ID for the input field
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

                                        # Buttons: Cancel and Add (Aligned to the right)
                                        html.Div(
                                            children=[
                                                html.Button(
                                                    "Cancel",
                                                    id="cancel-button",
                                                    n_clicks=0,
                                                    style={
                                                        "background-color": "red", 
                                                        "color": "white", 
                                                        "font-size": "14px",
                                                        "font-weight": "bold",
                                                        "border-radius": "5px",
                                                        "padding": "5px 40px", 
                                                        "margin-top": "40px", 
                                                        "margin-right": "30px", 
                                                        "border": "none", 
                                                        "cursor": "pointer"
                                                    }
                                                ),
                                                html.Button(
                                                    "Add",
                                                    id="add-button",
                                                    n_clicks=0,
                                                    style={
                                                        "background-color": "green", 
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
        html.Div(id="submit-status-add-med-record-new", style={"margin-top": "20px"}),
    ]
)

def add_medical_record_patient(app):
    @app.callback(
        [
            Output("submit-status-add-med-record-new", "children"),
            Output("date-picker-visit-add-auto", "date"),
            Output('medical-record-adding-data-store', 'data')
        ],
        [
            Input('url', 'pathname'),  # Trigger on URL change
            Input("add-button", "n_clicks")  # Keep button input for form submission
        ],
        [
            State("height-input-add", "value"),
            State("weight-input-add", "value"),
            State("blood-pressure-input-add", "value"),
            State("temp-input-add", "value"),
            State("consult-type-input-add", "value"),
            State("diagnosis-input-add", "value"),
            State("treatment-input-add", "value"),
            State("lab-res-input-add", "value"),
            State("note-input-add", "value"),
        ],
    )
    def add_patient(pathname, n_clicks, patient_height, patient_weight, record_bloodpressure, record_temperature, record_consultation_type, record_diagnosis, record_treatment, record_lab_result, record_side_note):
        print(f"Callback triggered. Pathname: {pathname}, n_clicks: {n_clicks}")

        # Extract patient_id from the URL pathname
        patient_id = None
        if pathname:
            segments = pathname.split('/')
            if len(segments) > 1:
                patient_id = segments[-1]
        print(f"Extracted patient_id: {patient_id}")

        if not patient_id:
            print("No patient ID provided.")
            raise PreventUpdate

        # Establish a connection to the database
        connection = create_connection()
        if not connection:
            print("Database connection failed.")
            return "Database connection failed.", None, None

        try:
            cursor = connection.cursor()

            # Check if the patient exists and insert height/weight if not
            cursor.execute("SELECT 1 FROM patient WHERE patient_id = %s", (patient_id,))
            result = cursor.fetchone()

            if not result:
                # Insert patient height and weight into the patient table if they are provided
                if patient_height is None or patient_weight is None:
                    print("Patient height and weight are required for new patients.")
                    return "Patient height and weight are required.", None, None

                print("Inserting patient data...")
                cursor.execute(
                    """
                    INSERT INTO patient (patient_id, patient_height, patient_weight)
                    VALUES (%s, %s, %s)
                    """,
                    (patient_id, patient_height, patient_weight)
                )
                connection.commit()
                print("Patient data inserted successfully.")

            else:
                # Update patient height and weight if the patient exists and new data is provided
                if patient_height is not None and patient_weight is not None:
                    print("Updating patient height and weight...")
                    cursor.execute(
                        """
                        UPDATE patient
                        SET patient_height = %s, patient_weight = %s
                        WHERE patient_id = %s
                        """,
                        (patient_height, patient_weight, patient_id)
                    )
                    connection.commit()
                    print("Patient data updated successfully.")

            # Fetch the latest appointment date
            cursor.execute("SELECT appointment_date FROM appointment WHERE patient_id = %s ORDER BY appointment_date DESC LIMIT 1", (patient_id,))
            appointment_result = cursor.fetchone()
            print(f"Fetched appointment_date: {appointment_result}")

            appointment_date_iso = None
            if appointment_result:
                appointment_date = appointment_result[0]
                if isinstance(appointment_date, datetime.date):
                    # Format the date to YYYY-MM-DD
                    appointment_date_iso = appointment_date.strftime('%Y-%m-%d')
                else:
                    print("Fetched appointment_date is not a datetime.date object.")
            
            print(f"Formatted appointment_date (ISO): {appointment_date_iso}")

            # If form was submitted, proceed with inserting the medical record
            if n_clicks:
                if not all([record_bloodpressure, record_temperature, record_consultation_type, record_diagnosis, record_treatment, record_lab_result, record_side_note]):
                    print("Some required fields are missing.")
                    return "Please fill in all fields.", appointment_date_iso, {'appointment_date': appointment_date_iso}

                # Insert medical record data
                print("Inserting medical record data...")
                cursor.execute(
                    """
                    INSERT INTO medical_record (patient_id, record_bloodpressure, record_temperature, record_consultation_type, record_diagnosis, record_treatment, record_lab_result, record_side_note)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (patient_id, record_bloodpressure, record_temperature, record_consultation_type, record_diagnosis, record_treatment, record_lab_result, record_side_note)
                )
                connection.commit()
                print("Medical record inserted successfully.")

                # Get the record_id of the newly inserted medical record
                cursor.execute("SELECT LAST_INSERT_ID()")
                record_id = cursor.fetchone()[0]
                print(f"Inserted record_id: {record_id}")

                # Insert record_id into the appointment table
                cursor.execute(
                    """
                    UPDATE appointment
                    SET record_id = %s
                    WHERE patient_id = %s AND appointment_date = %s
                    """,
                    (record_id, patient_id, appointment_date_iso)
                )
                connection.commit()
                print(f"record_id {record_id} inserted into appointment table.")

                return (
                    html.Div("Patient information and medical record added successfully!"),
                    appointment_date_iso,
                    {'appointment_date': appointment_date_iso}
                )

            return (
                html.Div(""),
                appointment_date_iso,
                {'appointment_date': appointment_date_iso}
            )

        except Exception as e:
            print(f"An error occurred: {e}")
            return f"An error occurred: {e}", None, None

        finally:
            print("Closing database connection.")
            close_connection(connection)