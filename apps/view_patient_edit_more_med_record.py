import dash_bootstrap_components as dbc
from dash import dcc, html, Output, Input, State, callback_context
from dash.exceptions import PreventUpdate
from apps.dbconnect import create_connection, close_connection
from urllib.parse import parse_qs
import time
from decimal import Decimal
from datetime import datetime
import json

def fetch_detailed_patient_info(patient_id):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            # Modified query to use appointment_date instead of record_date
            query = """
            WITH LatestRecord AS (
                SELECT 
                    m.patient_id,
                    m.record_id,
                    m.record_bloodpressure,
                    m.record_temperature,
                    m.record_consultation_type,
                    m.record_diagnosis,
                    m.record_treatment,
                    m.record_lab_result,
                    m.record_side_note,
                    a.appointment_date
                FROM medical_record m
                LEFT JOIN appointment a ON m.record_id = a.record_id
                WHERE m.patient_id = %s
                ORDER BY a.appointment_date DESC
                LIMIT 1
            )
            SELECT 
                p.patient_height,
                p.patient_weight,
                lr.record_bloodpressure,
                lr.record_temperature,
                lr.record_consultation_type,
                lr.record_diagnosis,
                lr.record_treatment,
                lr.record_lab_result,
                lr.record_side_note,
                lr.appointment_date
            FROM patient p
            LEFT JOIN LatestRecord lr ON p.patient_id = lr.patient_id
            WHERE p.patient_id = %s
            """
            cursor.execute(query, (patient_id, patient_id))
            data = cursor.fetchone()
            print(f"Raw data fetched for patient {patient_id}: {data}")
            return data
        except Exception as e:
            print(f"Database error: {e}")
            import traceback
            print(f"Traceback: {traceback.format_exc()}")
            return None
        finally:
            cursor.close()
            close_connection(connection)
    return None

# Define styles for the layout
styles = {
    "subHeader1": {
        "padding": "40px",
        "marginLeft": "60px"
    },
    "backViewMedicalRecords": {
        "fontSize": "18px",
        "marginTop": "-30px",
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
        dcc.Store(id='edit-medical-record-mode-data-store'),
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

        # Window - View Patient Medical Record - To Edit More Info
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
                                        "Edit Patient Medical Record",
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
                                                            id="height-input-edit-mod",  # ID for the input field
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
                                                            id="weight-input-edit-mod",  # ID for the input field
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
                                                            id="blood-pressure-input-edit-mod",  # ID for the input field
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
                                                            id="temp-input-edit-mod",  # ID for the input field
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
                                                            id="date-picker-appointment-edit-mod",
                                                            placeholder="YYYY-MM-DD",  # Changed to match expected format
                                                            display_format="YYYY-MM-DD",  # Changed to match expected format
                                                            style={
                                                                "margin-right": "168px",
                                                                "margin-bottom": "15px",
                                                                "width": "100px",
                                                            },
                                                            className="custom-date-picker"
                                                        )
                                                    ],
                                                    style={"margin-right": "20px", "text-align": "left"},  # Spacing and alignment
                                                ),
                                                # Consultation Type
                                                html.Div(
                                                    children=[
                                                        "Consultation Type",
                                                        html.Br(),  # Line break
                                                        dcc.Input(
                                                            id="consult-type-input-edit-mod",  # ID for the input field
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
                                                                id="diagnosis-input-edit-mod",  # ID for the input field
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
                                                                id="treatment-input-edit-mod",  # ID for the input field
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
                                                            id="lab-res-input-edit-mod",  # ID for the input field
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
                                                                id="note-input-edit-mod",  # ID for the input field
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
                                                        "margin-right": "20px", 
                                                        "border": "none", 
                                                        "cursor": "pointer"
                                                    }
                                                ),
                                                html.Button(
                                                    "Save",
                                                    id="save-button-edit",
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
                html.Div(id="save-status-medical-record-edit", children="")
    ]
)
 
def edit_medical_record_mode(app):
    # First callback to store the data
    @app.callback(
        Output('edit-medical-record-mode-data-store', 'data'),
        [Input('url', 'pathname')]
    )
    def store_patient_data(pathname):
        if not pathname:
            raise PreventUpdate
            
        try:
            patient_id = pathname.split('/')[-1]
            if not patient_id.isdigit():
                raise PreventUpdate
                
            data = fetch_detailed_patient_info(patient_id)
            if not data:
                return None
                
            # Convert Decimal and datetime objects to strings for JSON serialization
            processed_data = []
            for item in data:
                if isinstance(item, Decimal):
                    processed_data.append(str(float(item)))
                elif isinstance(item, datetime):
                    processed_data.append(item.strftime('%Y-%m-%d'))
                else:
                    processed_data.append(str(item) if item is not None else '')
                    
            print(f"Storing processed data: {processed_data}")
            return processed_data
            
        except Exception as e:
            print(f"Error in store_patient_data: {e}")
            return None

    # Second callback to update form fields
    @app.callback(
        [
            Output('height-input-edit-mod', 'value'),
            Output('weight-input-edit-mod', 'value'),
            Output('blood-pressure-input-edit-mod', 'value'),
            Output('temp-input-edit-mod', 'value'),
            Output('consult-type-input-edit-mod', 'value'),
            Output('diagnosis-input-edit-mod', 'value'),
            Output('treatment-input-edit-mod', 'value'),
            Output('lab-res-input-edit-mod', 'value'),
            Output('note-input-edit-mod', 'value'),
            Output('date-picker-appointment-edit-mod', 'date'),
        ],
        [Input('edit-medical-record-mode-data-store', 'data')]
    )
    def update_form_fields(stored_data):
        if not stored_data:
            print("No stored data available")
            return [''] * 9 + [None]
            
        print(f"Updating form with stored data: {stored_data}")
        
        try:
            # Return the values in the correct order
            return [
                stored_data[0],  # height
                stored_data[1],  # weight
                stored_data[2],  # blood pressure
                stored_data[3],  # temperature
                stored_data[4],  # consultation type
                stored_data[5],  # diagnosis
                stored_data[6],  # treatment
                stored_data[7],  # lab result
                stored_data[8],  # side note
                stored_data[9]   # appointment date
            ]
        except Exception as e:
            print(f"Error updating form fields: {e}")
            import traceback
            print(f"Traceback: {traceback.format_exc()}")
            return [''] * 9 + [None]
    
    @app.callback(
        Output('save-status-medical-record-edit', 'children'),
        [Input('save-button-edit', 'n_clicks')],
        [
            State('height-input-edit-mod', 'value'),
            State('weight-input-edit-mod', 'value'),
            State('blood-pressure-input-edit-mod', 'value'),
            State('temp-input-edit-mod', 'value'),
            State('consult-type-input-edit-mod', 'value'),
            State('diagnosis-input-edit-mod', 'value'),
            State('treatment-input-edit-mod', 'value'),
            State('lab-res-input-edit-mod', 'value'),
            State('note-input-edit-mod', 'value'),
            State('date-picker-appointment-edit-mod', 'date'),
            State('url', 'pathname')
        ]
    )
    def save_medical_record_changes(n_clicks, height, weight, blood_pressure, temperature,
                                  consultation_type, diagnosis, treatment, lab_result,
                                  side_note, appointment_date, pathname):
        if not n_clicks or not pathname:
            raise PreventUpdate

        patient_id = pathname.split('/')[-1]
        if not patient_id.isdigit():
            return "Invalid patient ID"

        connection = create_connection()
        if not connection:
            return "Database connection failed"

        try:
            cursor = connection.cursor()

            # First, update patient table
            patient_update_query = """
            UPDATE patient 
            SET patient_height = %s, patient_weight = %s
            WHERE patient_id = %s
            """
            cursor.execute(patient_update_query, (height, weight, patient_id))

            # Get the latest record_id for this patient
            get_record_query = """
            SELECT record_id 
            FROM medical_record 
            WHERE patient_id = %s 
            ORDER BY record_id DESC 
            LIMIT 1
            """
            cursor.execute(get_record_query, (patient_id,))
            record_id = cursor.fetchone()[0]

            # Update medical_record table
            medical_record_update_query = """
            UPDATE medical_record 
            SET record_bloodpressure = %s,
                record_temperature = %s,
                record_consultation_type = %s,
                record_diagnosis = %s,
                record_treatment = %s,
                record_lab_result = %s,
                record_side_note = %s
            WHERE record_id = %s AND patient_id = %s
            """
            cursor.execute(medical_record_update_query, (
                blood_pressure, temperature, consultation_type,
                diagnosis, treatment, lab_result, side_note,
                record_id, patient_id
            ))

            # Update appointment table
            appointment_update_query = """
            UPDATE appointment 
            SET appointment_date = %s
            WHERE record_id = %s
            """
            cursor.execute(appointment_update_query, (appointment_date, record_id))

            connection.commit()
            return "Medical record updated successfully!"

        except Exception as e:
            connection.rollback()
            print(f"Error saving medical record: {e}")
            return f"Error saving medical record: {str(e)}"

        finally:
            cursor.close()
            close_connection(connection)