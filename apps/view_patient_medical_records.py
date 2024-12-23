import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.exceptions import PreventUpdate
from urllib.parse import parse_qs
from apps.dbconnect import create_connection, close_connection
from dash.dependencies import Input, Output, State, ALL
import dash.exceptions as exceptions


# Define styles for the layout
styles = {
    "subHeader1": {
        "padding": "40px",
        "marginLeft": "60px"
    },
    "viewMedicalRecords": {
        "fontSize": "18px",
        "color": "#05066d",
        "marginTop": "-30px",
        "marginBottom": "50px",
    },
    "titleMedicalRecords": {
        "fontSize": "30px",
        "color": "#05066d",
        "fontWeight": "bold",
    },
    "divider1": {
        "width": "93%",
        "border": "2px solid #05066d",
        "marginTop": "-3px"
    },
    "divider2": {
        "width": "93%",
        "border": "2px solid #05066d",
        "marginTop": "-20px"
    },
    "patientRecords": {
        "fontSize": "18px",
        "color": "#05066d",
    },
}

# Set up routing and layout
layout = html.Div(
    children=[

        # Content 1
        html.Div(
            style=styles["subHeader1"],
            children=[          
                # Section 1 - Title and Description
                html.P(
                    children=[                
                        "Patient / Medical Records / ",  # Normal text
                        html.Span(
                            "View Patient Medical Records",  # Text to make bold and underlined
                            style={
                                "fontWeight": "bold",  # Bold text
                                "textDecoration": "underline",  # Underlined text
                            },
                        ),
                    ],
                    style=styles["viewMedicalRecords"],
                ),
                html.H2("Medical Records", style=styles["titleMedicalRecords"]),
                html.Hr(style=styles["divider1"]),  # Divider line
                
                # Section 2 - Dynamic Content (Patient Name and Button)
                html.Div(
                    style={
                        'display': 'flex',
                        'alignItems': 'center',
                        'gap': '10px',
                        'justifyContent': 'space-between',
                    },
                    children=[
                        # Patient's name display
                        html.H3(
                            id='patient-name',  # Dynamically updated patient name
                            style={
                                'margin': '0',
                                'fontSize': '20px',
                                'color': '#05066d',
                                'fontWeight': 'bold',
                            }
                        ),
                        
                        # Add new medical record button
                        html.Div(id='add-med-record-link'),


                        # Interval component for periodic updates
                        dcc.Interval(
                            id="interval-refresh",
                            interval=1000,  # Interval in milliseconds (1 second)
                            n_intervals=0,
                        )
                    ]
                ),
            ],
        ),


        # The table box
        html.Div(
            style={"padding": "0px"},
            children=[
                # Search for Medical Services
                html.Div(
                    style={"padding": "10px"},
                    children=[
                        # Table Container with smaller width
                        html.Table(
                            style={
                                "width": "85%",  # Reduced table width
                                "margin-left": "90px",  # Move the table to the left
                                "margin-top": "-30px",
                                "border": "1px solid black", 
                                "border-collapse": "collapse"
                            },
                            children=[
                                # Table Header Row
                                html.Tr(
                                    children=[
                                        html.Th(
                                            children=[
                                                "Search Patient Medical Records",
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
                                                # Date of Visit
                                                html.Div(
                                                    children=[
                                                        "Date of Visit",
                                                        html.Br(),  # Line break
                                                        dcc.DatePickerSingle(
                                                            id="date-picker-visit",
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
                                                    style={"text-align": "left", "color": "#05066d", "font-weight": "bold", "margin-right": "10px"},  # Align label and input field
                                                ),

                                                # Consultation Type Input
                                                html.Div(
                                                    children=[
                                                        "Consultation Type",
                                                        html.Br(),  # Line break
                                                        dcc.Input(
                                                            id="consult-type-input",  # ID for the input field
                                                            type="text",  # Type of the input field (number)
                                                            placeholder="ECG",  # Placeholder text for the input
                                                            style={"width": "300px", "padding": "5px", "font-style": "italic"}  # Reduced size for inline display
                                                        ),
                                                    ],
                                                    style={"text-align": "left", "color": "#05066d", "font-weight": "bold", "margin-left": "10px"},  # Align label and input field
                                                ),
                                            ],
                                            style={
                                                "padding-left": "40px", 
                                                "padding-top": "10px", 
                                                "padding-bottom": "10px",
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

        # Content 2
        html.Div(
            style=styles["subHeader1"],
            children=[

                # Section 2
                html.Hr(style=styles["divider2"]),
                html.H3("Patient Medical Records", style=styles["patientRecords"]),
            ],
        ),

        # Table list for the Medical Records 
        html.Div(
        style={"padding": "0px"},
        children=[
        html.Div(
            style={"padding": "10px"},
            children=[
                html.Div(id='medical-records-table-list'),  # Placeholder for dynamic table
            ],
        ),
    ],
),
    ]
)

def view_patient(app):
    # Callback to update the patient name
    @app.callback(
        Output('patient-name', 'children'),
        [Input('url', 'pathname'),
         Input('interval-refresh', 'n_intervals')]  # Trigger periodically
    )
    def update_patient_name(pathname, n_intervals):
        patient_id = None

        if pathname:
            print(f"Initial pathname: {pathname}")  # Debugging: check the pathname
            segments = pathname.split('/')
            print(f"Path segments: {segments}")  # Debugging: check the split segments

            # Extract patient_id based on the pathname structure
            if pathname.startswith('/view_patient_medical_records') or pathname.startswith('/view_patient_add_medical_record') or pathname.startswith('/view_medical_records_history') or pathname.startswith('/edit_patient_more_medical_records'):
                if len(segments) > 1:
                    patient_id = segments[-1]

        print(f"Extracted patient_id: {patient_id}")  # Debugging: check the extracted patient_id

        # Fetch data if patient_id exists
        if patient_id:
            connection = create_connection()  # Replace with your actual DB connection logic
            data = None

            if connection:
                try:
                    cursor = connection.cursor()
                    query = """
                    SELECT patient_first_name, patient_last_name
                    FROM patient
                    WHERE patient_id = %s
                    """
                    cursor.execute(query, (patient_id,))
                    result = cursor.fetchone()

                    if result:
                        patient_first_name, patient_last_name = result
                        full_name = f"Patient Name: {patient_first_name} {patient_last_name}"
                        data = full_name
                    else:
                        print(f"No data found for patient_id: {patient_id}")
                        data = "Patient not found"
                except Exception as e:
                    print(f"Error fetching medical record: {e}")
                    data = "Error fetching data"
                finally:
                    close_connection(connection)  # Close connection after the query

            return data

        return "Patient not found"  # Default message if patient_id is not found

    # Callback for "Add New Medical Record" button
    @app.callback(
    Output('add-med-record-link', 'children'),
    [Input('url', 'pathname')],
    allow_duplicate=True  # Allow duplicate outputs
    )
    def update_link(pathname):
        # Limit this callback to specific pathnames
        if not pathname or not pathname.startswith('/view_patient_medical_records/'):
            print(f"Ignoring pathname for button generation: {pathname}")  # Debugging output
            raise PreventUpdate  # Do not process further if the URL doesn't match

        # Extract patient_id 
        segments = pathname.split('/')
        print(f"Path segments for button: {segments}")  # Debugging output
        patient_id = segments[-1] if len(segments) > 2 else None

        # Generate the button if patient_id is valid
        if patient_id:
            print(f"Dynamic button generated for patient_id: {patient_id}")
            return dcc.Link(
                html.Button(
                    'Add New Medical Record',
                    id='view-patient-med-records-button',
                    n_clicks=0,
                    style={
                        'backgroundColor': '#b0c5ff',
                        'color': '#05066d',
                        'margin-right': '80px',
                        'fontSize': '14px',
                        'fontWeight': 'bold',
                        'padding': '5px 20px',
                        'border': '1px solid',
                        'borderRadius': '5px',
                        'cursor': 'pointer',
                        'boxShadow': '0px 4px 6px rgba(0, 0, 0, 0.1)',
                        'transition': 'background-color 0.3s ease',
                    },
                ),
                href=f'/view_patient_add_medical_record/{patient_id}'  # Dynamic href
            )

        print("No patient_id found in URL for button")
        raise PreventUpdate
    
    @app.callback(
    Output('medical-records-table-list', 'children'),
    [
        Input('url', 'pathname'),
        Input('interval-refresh', 'n_intervals'),
        Input({'type': 'delete-button', 'index': ALL}, 'n_clicks'),
        Input('date-picker-visit', 'date'),
        Input('consult-type-input', 'value')
    ]
    )
    def manage_medical_records(pathname, n_intervals, n_clicks, selected_date, consult_type):
        # Handle deletion logic (unchanged)...
        if n_clicks and any(n_clicks):
            # Your existing deletion code here...
            pass

        patient_id = None
        if pathname:
            segments = pathname.split('/')
            if len(segments) > 1:
                patient_id = segments[-1]
                if patient_id.isdigit():
                    patient_id = int(patient_id)
                else:
                    return html.Div("Invalid patient ID in URL.")

        if not patient_id:
            return html.Div("No patient selected or invalid URL.")

        connection = create_connection()
        if connection:
            try:
                cursor = connection.cursor()

                # Build the query with optional filters
                base_query = """
                SELECT 
                    COALESCE(a.appointment_date, 'No Appointment') AS appointment_date, 
                    m.record_consultation_type
                FROM medical_record m
                LEFT JOIN appointment a ON m.record_id = a.record_id
                LEFT JOIN patient p ON a.patient_id = p.patient_id
                WHERE p.patient_id = %s
                """
                query_params = [patient_id]

                # Add date filter if selected
                if selected_date:
                    base_query += " AND DATE(a.appointment_date) = %s"
                    query_params.append(selected_date)

                # Add consultation type filter if provided
                if consult_type:
                    base_query += " AND m.record_consultation_type ILIKE %s"
                    query_params.append(f"%{consult_type}%")

                cursor.execute(base_query, tuple(query_params))
                records = cursor.fetchall()

                if not records:
                    return html.Table(
                        style={
                            "width": "85%",
                            "margin-left": "88px",
                            "margin-top": "-30px",
                            "margin-right": "auto",
                            "border": "1px solid black",
                            "border-collapse": "collapse",
                            "background-color": "#fff",
                            "box-shadow": "0 2px 4px rgba(0,0,0,0.1)",
                        },
                        children=[
                            # Table Header
                            html.Tr([
                                html.Th(
                                    header,
                                    style={
                                        "padding": "12px",
                                        "text-align": "center",
                                        "font-weight": "bold",
                                        "background-color": "#05066d",
                                        "color": "white",
                                        "border": "1px solid black",
                                    },
                                ) for header in [
                                    "Date of Visit", "Consultation Type", "View", "Edit", "Delete"
                                ]
                            ]),
                            html.Tr([
                                html.Td(
                                    "No matching records found.",
                                    colSpan=5,
                                    style={
                                        "padding": "12px",
                                        "text-align": "center",
                                        "border": "1px solid black",
                                        "background-color": "#f9f9f9",
                                        "font-weight": "bold",
                                        "color": "red",
                                    }
                                )
                            ])
                        ]
                    )

                # Rest of your table generation code remains the same...
                rows = []
                for record in records:
                    appointment_date = record[0] if record[0] is not None else "No Appointment"
                    consultation_type = record[1]
                    rows.append(
                        html.Tr([
                            html.Td(
                                appointment_date if isinstance(appointment_date, str) else appointment_date.strftime("%m/%d/%Y"),
                                style={"padding": "12px", "text-align": "center", "border": "1px solid black", "background-color": "#f9f9f9"}
                            ),
                            html.Td(
                                consultation_type,
                                style={"padding": "12px", "text-align": "center", "border": "1px solid black", "background-color": "#f9f9f9"}
                            ),
                            # Your existing button cells remain the same...
                            html.Td(
                                dcc.Link(
                                    html.Button(
                                        "View",
                                        style={
                                            "padding": "5px 20px",
                                            "background-color": "#4CAF50",
                                            "color": "white",
                                            "border": "none",
                                            "cursor": "pointer",
                                            "border-radius": "5px",
                                        },
                                    ),
                                    href=f'/view_medical_records_history/{patient_id}'
                                ),
                                style={"padding": "12px", "text-align": "center", "border": "1px solid black", "background-color": "#f9f9f9"}
                            ),
                            html.Td(
                                dcc.Link(
                                    html.Button(
                                        "Edit",
                                        style={
                                            "padding": "5px 20px",
                                            "background-color": "#b0c5ff",
                                            "color": "#05066d",
                                            "border": "none",
                                            "cursor": "pointer",
                                            "border-radius": "5px",
                                        },
                                    ),
                                    href=f'/edit_patient_more_medical_records/{patient_id}'
                                ),
                                style={"padding": "12px", "text-align": "center", "border": "1px solid black", "background-color": "#f9f9f9"}
                            ),
                            html.Td(
                                html.Button(
                                    "Delete",
                                    id={'type': 'delete-button', 'index': record[0]},
                                    style={
                                        "padding": "5px 20px",
                                        "background-color": "red",
                                        "color": "white",
                                        "border": "none",
                                        "cursor": "pointer",
                                        "border-radius": "5px",
                                    },
                                ),
                                style={"padding": "12px", "text-align": "center", "border": "1px solid black", "background-color": "#f9f9f9"}
                            ),
                        ])
                    )

                return html.Table(
                    style={
                        "width": "85%",
                        "margin-left": "88px",
                        "margin-top": "-30px",
                        "margin-right": "auto",
                        "border": "1px solid black",
                        "border-collapse": "collapse",
                        "background-color": "#fff",
                        "box-shadow": "0 2px 4px rgba(0,0,0,0.1)",
                    },
                    children=[
                        html.Tr([
                            html.Th(
                                header,
                                style={
                                    "padding": "12px",
                                    "text-align": "center",
                                    "font-weight": "bold",
                                    "background-color": "#05066d",
                                    "color": "white",
                                    "border": "1px solid black",
                                },
                            ) for header in [
                                "Date of Visit", "Consultation Type", "View", "Edit", "Delete"
                            ]
                        ]),
                        *rows,
                    ]
                )

            except Exception as e:
                import traceback
                print(f"Error fetching records: {e}")
                traceback.print_exc()
                return html.Div(f"Error fetching medical records: {e}")
            finally:
                close_connection(connection)
        else:
            return html.Div("Database connection error.")