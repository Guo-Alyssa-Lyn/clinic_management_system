import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output
from dash.exceptions import PreventUpdate
from apps.dbconnect import create_connection, close_connection

import pandas as pd

def fetch_data():
    # Create a connection to the database
    connection = create_connection()
    data = []  # Initialize an empty list to store formatted data

    try:
        # First query to fetch patient data
        query_patient = """
        SELECT 
            p.patient_id, 
            CONCAT(p.patient_first_name, ' ', p.patient_middle_name, ' ', p.patient_last_name) AS full_name, 
            p.patient_contact_number
        FROM patient p;
        """

        cursor = connection.cursor()
        cursor.execute(query_patient)
        patient_rows = cursor.fetchall()

        # Debug: Print raw data from the query
        print("Fetched Patient Rows:", patient_rows)

        # Second query to fetch appointment data
        query_appointment = """
        SELECT 
            a.patient_id, 
            a.appointment_id, 
            a.appointment_date, 
            a.appointment_time
        FROM appointment a;
        """

        cursor.execute(query_appointment)
        appointment_rows = cursor.fetchall()

        # Debug: Print raw data from the query
        print("Fetched Appointment Rows:", appointment_rows)

        # Process each patient and match with appointment data
        for patient_row in patient_rows:
            patient_id = patient_row[0]
            full_name = patient_row[1]
            contact_number = patient_row[2]
            
            # Find the corresponding appointment data for each patient
            patient_appointments = [
                appointment for appointment in appointment_rows if appointment[0] == patient_id
            ]
            
            for appointment in patient_appointments:
                appointment_id = appointment[1]
                appointment_date = appointment[2]
                appointment_time = appointment[3]
                
                # Appending formatted data to the list
                data.append({
                    'patient_id': patient_id,
                    'full_name': full_name,
                    'contact_number': contact_number,
                    'appointment_id': appointment_id,
                    'appointment_date': appointment_date,
                    'appointment_time': appointment_time,
                })

    except Exception as e:
        print(f"Error: {e}")
        return []

    finally:
        cursor.close()  # Close the cursor
        close_connection(connection)  # Ensure the connection is closed properly

    # Debug: Print the formatted data to be returned
    print("Formatted Data:", data)
    return data

headers = ["ID", "Patient Name", "Appointment Date", "Appointment Time", "Contact Number", "Edit"]

# Define styles for the layout
styles = {
    "header": {
        "display": "flex",
        "justifyContent": "space-between",  # Title on the left, links on the right
        "alignItems": "center",  # Vertically center items
        "backgroundColor": "#b0c5ff",
        "padding": "30px 20px",
        "color": "#05066d",
        "fontFamily": "'Cocomat Pro', sans-serif",
    },
    "title": {
        "fontSize": "24px",
        "fontWeight": "bold",
        "paddingLeft": "30px",
    },
    "navLinks": {
        "display": "flex",
        "gap": "80px",  # Space between links
    },
    "link": {
        "color": "#05066d",
        "textDecoration": "none",
        "fontSize": "18px",
        "transition": "color 0.3s ease",
    },
    "linkLast": {
        "color": "#05066d",
        "textDecoration": "none",
        "fontSize": "18px",
        "paddingRight": "50px",
        "transition": "color 0.3s ease",
    },
    "subHeader1": {
        "padding": "40px",
        "marginLeft": "60px"
    },
    "bookAppointment": {
        "fontSize": "18px",
        "color": "#05066d",
        "marginTop": "-27px",
        "margin-bottom": "50px"
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
    "appointSchedTitle": {
        "fontSize": "18px",
        "color": "#05066d",
    },
}

# Set up routing and layout
layout = html.Div(
    children=[

        # Section 1
        html.Div(
            style=styles["subHeader1"],
            children=[
                # Section 1
                html.P(
                    children=[
                        "Appointment / ",  # Normal text
                        html.Span(
                            "Book an Appointment",  # Text to make bold and underlined
                            style={
                                "fontWeight": "bold",  # Bold text
                                "textDecoration": "underline",  # Underline text
                            },
                        ),
                    ],
                    style=styles["bookAppointment"],
                ),
                html.P("Appointment Schedule", style=styles["appointSched"]),
                html.Hr(style=styles["divider1"]),
                dcc.Link(
                    html.Button(
                        'Add New Appointment',
                        id='add-appoint-button',
                        n_clicks=0,
                        style={
                            'backgroundColor': '#b0c5ff',  # Button background color
                            'color': '#05066d',  # Button text color
                            'fontSize': '14px',  # Font size
                            'fontWeight': 'bold',  # Bold text
                            'marginBottom': '-200px',
                            'padding': '5px 10px',  # Padding around text
                            'border': '1px solid',  # Border
                            'borderRadius': '5px',  # Rounded corners
                            'cursor': 'pointer',  # Pointer cursor on hover
                            'boxShadow': '0px 4px 6px rgba(0, 0, 0, 0.1)',  # Shadow effect
                            'transition': 'background-color 0.3s ease',  # Smooth transition for hover effect
                        },
                    ),
                    href='/add_appointment'  # Replace with the target page URL you want to link to
                ),
            ],
        ),


         # The table box
            html.Div(
            style={"padding": "0px"},
            children=[
                # Search for Search Appointment Schedule
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
                                                "Search Appointment Schedule",
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
                                            # Full Name Input
                                            html.Div(
                                                children=[
                                                    "Patient Name",
                                                    html.Br(),  # Line break
                                                    dcc.Input(
                                                        id="patient-name-input",  # ID for the input field
                                                        type="text",  # Type of the input field (text)
                                                        placeholder="Juan Dela Cruz",  # Placeholder text for the input
                                                        style={"width": "350px", "padding": "5px", "font-style": "italic"}  # Reduced size for inline display
                                                    ),
                                                ],
                                                style={"text-align": "left", "color": "#05066d", "font-weight": "bold", "margin-right": "10px"},  # Align label and input field
                                            ),

                                            # Appointment Date Input
                                            html.Div(
                                                children=[
                                                    "Appointment Date",
                                                    html.Br(),  # Line break
                                                    dcc.DatePickerSingle(
                                                            id="date-picker-appoint",
                                                            placeholder="mm/dd/yyyy",  # Placeholder format
                                                            display_format="MM/DD/YYYY",  # Display format
                                                            style={
                                                                "margin-right": "183px",
                                                                "margin-bottom": "10px",  # Adjusted margin for bottom spacing
                                                                "width": "100px",  # Set width to 100px
                                                            },
                                                            className="custom-date-picker"  # Add a custom class for specific targeting
                                                        ),
                                                ],
                                                style={"text-align": "left", "color": "#05066d", "font-weight": "bold", "margin-left": "10px"},  # Align label and input field
                                            ),

                                            # Appointment Time Input
                                            html.Div(
                                                children=[
                                                    "Appointment Time",
                                                    html.Br(),  # Line break
                                                    dcc.Input(
                                                        id="time-input",  # ID for the input field
                                                        type="text",  # Type of the input field (text)
                                                        placeholder="00:00 AM",  # Placeholder text for the input
                                                        style={"width": "350px", "padding": "5px", "font-style": "italic"}  # Reduced size for inline display
                                                    ),
                                                ],
                                                style={"text-align": "left", "color": "#05066d", "font-weight": "bold", "margin-left": "10px"},  # Align label and input field
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

        # Section 2 - Medical Services
        html.Div(
            style=styles["subHeader1"],
            children=[

                # Section 2
                html.Hr(style=styles["divider2"]),
                html.H3("Appointment Schedule", style=styles["appointSchedTitle"]),
            ],
        ),

   

    # Table for Appointment Schedule List
    html.Div(
        style={"padding": "0px"},
        children=[
        # Interval to trigger automatic updates
        dcc.Interval(
            id="interval-refresh",
            interval=1 * 1000,  # Trigger every 1 second
            n_intervals=0  # Start counting from 0
        ),

        html.Div(
            style={"padding": "10px"},
            children=[
                # Table Container
                html.Table(
                    style={
                        "width": "85%",
                        "margin-left": "88px",
                        "margin-right": "auto",
                        "margin-top": "-40px",
                        "border": "1px solid black",
                        "border-collapse": "collapse",
                    },
                    children=[
                        # Table Header
                        html.Tr(
                            children=[
                                html.Th(
                                    header,
                                    style={
                                        "padding": "12px",
                                        "text-align": "center",
                                        "font-weight": "bold",
                                        "background-color": "#05066d",
                                        "color": "white",
                                        "border": "1px solid black",
                                        "width": f"{100 / len(headers)}%",
                                    },
                                ) for header in headers
                            ],
                        ),
                        # Table Body: Dynamically populate rows from database data
                        html.Tbody(id="book-appointment-table-body")
                    ],
                ),
            ],
        ),
    ],
),
    ]
)

def book_appointment_display(app):
    # Callback to update the table body with filtered data
    @app.callback(
        Output("book-appointment-table-body", "children"),
        [
            Input("interval-refresh", "n_intervals"),  # Trigger on interval updates
            Input("patient-name-input", "value"),  # Filter by patient name
            Input("date-picker-appoint", "date"),  # Filter by appointment date
            Input("time-input", "value")  # Filter by appointment time
        ]
    )
    def update_table(n_intervals, patient_name, appointment_date, appointment_time):
        # Fetch data
        patients = fetch_data()

        # Filter data based on the input values
        if patient_name:
            patients = [patient for patient in patients if patient_name.lower() in patient['full_name'].lower()]
        
        if appointment_date:
            # Convert the datetime.date to string in 'YYYY-MM-DD' format
            appointment_date = appointment_date.strip()  # Remove spaces
            patients = [patient for patient in patients if patient['appointment_date'].strftime('%Y-%m-%d') == appointment_date]

        if appointment_time:
            # Ensure both appointment_time and input time are in the same format 'HH:MM'
            appointment_time = appointment_time.strip()  # Remove any extra spaces
            patients = [patient for patient in patients if patient['appointment_time'] == appointment_time]

        if not patients:
            # Return a message if no data matches the filters
            return [html.Tr([html.Td("No data available", colSpan=6, style={
                "text-align": "center", "padding": "10px"})])]

        # Generate table rows
        return [
            html.Tr(
                children=[
                    html.Td(patient['patient_id'], style={"text-align": "center", "padding": "10px", "border": "1px solid black"}),
                    html.Td(patient['full_name'], style={"text-align": "center", "padding": "10px", "border": "1px solid black"}),
                    html.Td(patient['appointment_date'], style={"text-align": "center", "padding": "10px", "border": "1px solid black"}),
                    html.Td(patient['appointment_time'], style={"text-align": "center", "padding": "10px", "border": "1px solid black"}),
                    html.Td(patient['contact_number'], style={"text-align": "center", "padding": "10px", "border": "1px solid black"}),
                    html.Td(
                        html.A(
                            "Edit",
                            href=f"/edit_appointment?appointment_id={patient['appointment_id']}",   # Link to the edit page with appointment_id
                            id=f"edit-{patient['patient_id']}",
                            style={
                                "padding": "1px 30px",
                                "background-color": "#b0c5ff",
                                "color": "#05066d",
                                "border-radius": "5px",
                                "text-align": "center",
                                "text-decoration": "none",  # Remove the underline for the link
                                "border": "none"
                            }
                        ),
                        style={"text-align": "center", "padding": "10px", "border": "1px solid black"}
                    ),
                ],
                style={"border": "none"}
            )
            for patient in patients
        ]