import dash_bootstrap_components as dbc
from dash import dcc, html, Output, Input, State
from dash.exceptions import PreventUpdate
from apps.dbconnect import create_connection, close_connection
from urllib.parse import parse_qs
import time

def fetch_service_details(appointment_id):
    connection = create_connection()
    data = None
    if connection: 
        cursor = connection.cursor()
        query = """
        SELECT appointment.appointment_date, appointment.appointment_time,
               CONCAT(patient.patient_first_name, ' ', patient.patient_last_name) AS patient_name,
               patient.patient_contact_number,
               appointment.appointment_status
        FROM appointment
        JOIN patient ON appointment.patient_id = patient.patient_id
        WHERE appointment.appointment_id = %s
        """
        cursor.execute(query, (appointment_id,))
        result = cursor.fetchone()
        if result:
            data = {
                'appointment_date': result[0],
                'appointment_time': result[1],
                'patient_name': result[2],
                'patient_contact_number': result[3],
                'appointment_status': result[4] if result[4] else 'Waiting In Line'
            }
        print(f"Query result: {data}")
        cursor.close()
        close_connection(connection)
    return data

# Define styles for the layout
styles = {
    "subHeader1": {
        "padding": "40px",
        "marginLeft": "60px"
    },
    "backAppointmentSched": {
        "fontSize": "18px",
        "color": "#05066d",
        "marginTop": "-27px",
    },
    "appointSched": {
        "fontWeight": "bold",
        "fontSize": "30px",
        "color": "#05066d",
    },
    "divider1": {
        "width": "93%",
        "border": "2px solid #05066d",
        "marginTop": "-15px"
    },
    "divider2": {
        "width": "93%",
        "border": "2px solid #05066d",
        "marginTop": "-30px"
    },
    "medicalServices2": {
        "fontSize": "18px",
        "color": "#05066d",
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
                                "Back to Appointment Schedule Page" 
                            ],
                            href="/book_appointment",  # Link target
                            style={
                                **styles["backAppointmentSched"],  # Apply existing styles
                                "text-decoration": "none",  # Remove underline
                                "color": "inherit"  # Ensure link text inherits color from parent
                            },
                        ),
                    ],
                    style={"margin-bottom": "50px"},
                ),
                html.P("Appointments Schedule", style=styles["appointSched"]),
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
                                        "Edit Appointment Schedule",
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
                                                        "Patient Name",
                                                        html.Br(),  # Line break
                                                        dcc.Input(
                                                            id="full-name-input-edit-mode",  # ID for the input field
                                                            type="text",  # Type of the input field (text)
                                                            placeholder="Juan Dela Cruz",  # Placeholder text for the input
                                                            style={"width": "250px", "padding": "5px", "margin-bottom": "10px", "font-style": "italic"}  # Input style
                                                        ),
                                                    ],
                                                    style={"margin-right": "20px", "text-align": "left"},  # Spacing and alignment
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
                                                # Appointment Date
                                                html.Div(
                                                    children=[
                                                        "Appointment Date",
                                                        html.Br(),  # Line break
                                                        dcc.DatePickerSingle(
                                                            id="date-picker-appoint-edit-mode",
                                                            placeholder="MM/DD/YYYY",  # Placeholder format
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
                                                # Appointment Time
                                                html.Div(
                                                    children=[
                                                        "Appointment Time",
                                                        html.Br(),  # Line break
                                                        dcc.Input(
                                                            id="time-input-edit-mode",  # ID for the input field
                                                            type="text",  # Type of the input field (text)
                                                            placeholder="00:00 AM",  # Placeholder text for the input
                                                            style={"width": "250px", "padding": "5px", "margin-right": "20px", "font-style": "italic"}  # Input style
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
                                                # Contact Number
                                                html.Div(
                                                    children=[
                                                        "Contact Number",
                                                        html.Br(),  # Line break
                                                        dcc.Input(
                                                            id="contact-input-edit-mode",  # ID for the input field
                                                            type="number",  # Type of the input field (text)
                                                            placeholder="09xx xxx xxx",  # Placeholder text for the input
                                                            style={"width": "250px", "padding": "5px", "margin-bottom": "50px", "font-style": "italic"}  # Input style
                                                        ),
                                                    ],
                                                    style={"margin-right": "20px", "text-align": "left"},  # Spacing and alignment
                                                ),

                                            html.Div(
                                                    children=[
                                                        "Appointment Status",
                                                        html.Br(),
                                                        dcc.RadioItems(
                                                            id="appointment-status-edit",
                                                            options=[
                                                                {"label": "Waiting In Line", "value": "Waiting In Line"},
                                                                {"label": "Served", "value": "Served"},
                                                            ],
                                                            style={
                                                                "width": "250px",
                                                                "margin-right": "20px",
                                                                "margin-top": "5px",
                                                            },
                                                            labelStyle={
                                                                "display": "inline-block",
                                                                "margin-right": "10px",
                                                            },
                                                        ),
                                                    ],
                                                    style={
                                                        "margin-right": "20px",
                                                        "margin-top": "5px",
                                                        "text-align": "left",
                                                        "min-width": "300px",
                                                    },
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
                                                    href="/book_appointment",  # Replace with the desired link
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
        html.Div(id='save-status-appointment'),
    ]
)

def edit_mode_appointment(app):
    # Store data callback
    @app.callback(
        Output('appointment-data-store', 'data'),
        Input("url", "search")
    )
    def fetch_and_store_data(search):
        if not search:
            raise PreventUpdate

        query_params = parse_qs(search[1:])
        appointment_id = query_params.get('appointment_id', [None])[0]
        
        if appointment_id:
            appointment_data = fetch_service_details(appointment_id)
            if appointment_data:
                return appointment_data
        
        return {
            'patient_name': '',
            'appointment_date': '',
            'appointment_time': '',
            'patient_contact_number': '',
            'appointment_status': 'Waiting In Line'
        }
    
    @app.callback(
        [
            Output('full-name-input-edit-mode', 'value'),
            Output('date-picker-appoint-edit-mode', 'date'),
            Output('time-input-edit-mode', 'value'),
            Output('contact-input-edit-mode', 'value'),
            Output('appointment-status-edit', 'value'),
        ],
        Input('appointment-data-store', 'data')
    )
    def update_input_fields(appointment_data):
        if not appointment_data:
            raise PreventUpdate
            
        return (
            appointment_data.get('patient_name', ''),
            appointment_data.get('appointment_date', ''),
            appointment_data.get('appointment_time', ''),
            appointment_data.get('patient_contact_number', ''),
            appointment_data.get('appointment_status', 'Waiting In Line'),
        )

    # Save changes callback
    @app.callback(
        Output('save-status-appointment', 'children'),
        Input('save-button', 'n_clicks'),
        [
            State('full-name-input-edit-mode', 'value'),
            State('date-picker-appoint-edit-mode', 'date'),
            State('time-input-edit-mode', 'value'),
            State('contact-input-edit-mode', 'value'),
            State('appointment-status-edit', 'value'),
            State('url', 'search')
        ]
    )
    def save_appointment_changes(n_clicks, patient_name, appointment_date, 
                               appointment_time, contact_number, 
                               appointment_status, search):
        if not n_clicks:
            raise PreventUpdate

        # Form validation
        if not all([patient_name, appointment_date, appointment_time, 
                   contact_number, appointment_status]):
            return html.Div("Error: All fields are required", 
                          style={'color': 'red'})

        # Get appointment_id from URL
        query_params = parse_qs(search[1:])
        appointment_id = query_params.get('appointment_id', [None])[0]
        
        if not appointment_id:
            return html.Div("Error: No appointment ID found", 
                          style={'color': 'red'})

        try:
            # Database connection
            connection = create_connection()
            if not connection:
                return html.Div("Error: Database connection failed", 
                              style={'color': 'red'})

            cursor = connection.cursor()

            # Update appointment
            update_query = """
                UPDATE appointment 
                SET appointment_date = %s,
                    appointment_time = %s,
                    appointment_status = %s
                WHERE appointment_id = %s
            """
            
            cursor.execute(update_query, (
                appointment_date,
                appointment_time,
                appointment_status,
                appointment_id
            ))
            
            # Update patient information
            update_patient_query = """
                UPDATE patient 
                SET patient_contact_number = %s
                WHERE patient_id = (
                    SELECT patient_id 
                    FROM appointment 
                    WHERE appointment_id = %s
                )
            """

            cursor.execute(update_patient_query, (
                contact_number,
                appointment_id
            ))
            
            connection.commit()
            cursor.close()
            close_connection(connection)
            
            return html.Div("Appointment updated successfully!", 
                          style={'color': 'green'})
            
        except Exception as e:
            print(f"Error updating appointment: {str(e)}")
            return html.Div(f"Error updating appointment: {str(e)}", 
                          style={'color': 'red'})

    return app