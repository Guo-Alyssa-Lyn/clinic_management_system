import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output
from dash.exceptions import PreventUpdate
from apps.dbconnect import create_connection, close_connection

import pandas as pd

# Function to fetch data from the database
def fetch_data():
    connection = create_connection()
    
    try:
        query = """
        SELECT doctor_id, doctor_name, doctor_specialization, doctor_availability_date, doctor_availability_time
        FROM doctor;
        """
        
        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        
        # Processing the doctor_availability_time
        processed_result = []
        for row in result:
            doctor_id, doctor_name, doctor_specialization, doctor_availability_date, doctor_availability_time = row
            # Split the time range (e.g., '10:00 AM - 2:00 PM')
            if doctor_availability_time:
                time_parts = doctor_availability_time.split(" - ")
                if len(time_parts) == 2:
                    start_time = time_parts[0].strip()  # '10:00 AM'
                    end_time = time_parts[1].strip()    # '2:00 PM'
                else:
                    start_time = doctor_availability_time.strip()
                    end_time = None
            else:
                start_time = end_time = None

            processed_result.append((doctor_id, doctor_name, doctor_specialization, doctor_availability_date, start_time, end_time))
        
        return processed_result
    
    except Exception as e:
        print(f"Error: {e}")
        return []
    
    finally:
        cursor.close()
        close_connection(connection)

# Fetch distinct dropdown options from the database
def get_dropdown_options():
    doctors = fetch_data()
    doctor_names = sorted(set(doctor[1] for doctor in doctors))  # Unique doctor names
    specializations = sorted(set(doctor[2] for doctor in doctors))  # Unique specializations
    
    doctor_name_options = [{'label': name, 'value': name} for name in doctor_names]
    specialization_options = [{'label': spec, 'value': spec} for spec in specializations]
    
    return doctor_name_options, specialization_options

# Define the updated table headers
headers = ["ID", "Doctor Name", "Specialization", "Date Availability", "Time Availability (Start)", "Time Availability (End)", "Edit"]

# Define styles for the layout
styles = {
    "subHeader1": {
        "padding": "40px",
        "marginLeft": "60px"
    },
    "docSchedule": {
        "fontSize": "18px",
        "color": "#05066d",
        "marginTop": "-30px",
        "margin-bottom": "50px"
    },
    "docSchedTitle": { 
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
    "docSchedule2": {
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
                            "Doctors Schedule",  # Text to make bold and underlined
                            style={
                                "fontWeight": "bold",  # Bold text
                                "textDecoration": "underline",  # Underlined text
                            },
                        ),
                    ],
                    style=styles["docSchedule"],
                ),
                html.P("Doctors Schedule", style=styles["docSchedTitle"]),
                html.Hr(style=styles["divider1"]),
                dcc.Link(
                    html.Button(
                        'Add New Doctor',
                        id='add-doctor-button',
                        n_clicks=0,
                        style={
                            'backgroundColor': '#b0c5ff',  # Green background
                            'color': '#05066d',  # Text color
                            'fontSize': '14px',  # Font size
                            'fontWeight': 'bold',  # Bold text
                            'marginBottom': '-200px',
                            'padding': '5px 10px',  # Padding
                            'border': '1px solid',  # Border
                            'borderRadius': '5px',  # Rounded corners
                            'cursor': 'pointer',  # Pointer cursor
                            'boxShadow': '0px 4px 6px rgba(0, 0, 0, 0.1)',  # Shadow effect
                            'transition': 'background-color 0.3s ease',  # Smooth hover transition
                        },
                    ),
                    href='/add_doctor'  # Replace with the URL of the page you want to link to
                ),
            ],
        ),


        # The table box
        html.Div(
            style={"padding": "0px"},
            children=[
                # Search Bar for finding Doctors
                html.Div(
                    style={"padding": "10px"},
                    children=[
                        # Table Container with smaller width
                        html.Table(
                            style={
                                "width": "85%",
                                "margin-left": "90px",
                                "margin-top": "-30px",
                                "border": "1px solid black",
                                "border-collapse": "collapse"
                            },
                            children=[
                                # Table Header Row
                                html.Tr(
                                    children=[
                                        html.Th(
                                            children=["Search Doctor"],
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
                                                # Doctor Name Input
                                                html.Div(
                                                    children=[
                                                        "Doctor Name",
                                                        html.Br(),
                                                        dcc.Dropdown(
                                                            id="doctor-full-name",
                                                            placeholder="Select doctor",
                                                            options=[],  # Dynamically populated
                                                            value=None,
                                                            style={"width": "350px", "font-style": "italic"}
                                                        ),
                                                    ],
                                                    style={
                                                        "text-align": "left",
                                                        "color": "#05066d",
                                                        "font-weight": "bold",
                                                        "margin-right": "10px"
                                                    },
                                                ),

                                                # Specialization Input
                                                html.Div(
                                                    children=[
                                                        "Specialization",
                                                        html.Br(),
                                                        dcc.Dropdown(
                                                            id="specialization-name",
                                                            placeholder="Select specialization",
                                                            options=[],  # Dynamically populated
                                                            value=None,
                                                            style={"width": "350px", "font-style": "italic"}
                                                        ),
                                                    ],
                                                    style={
                                                        "text-align": "left",
                                                        "color": "#05066d",
                                                        "font-weight": "bold",
                                                        "margin-left": "10px"
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
                                                "display": "flex",
                                                "flex-direction": "row",
                                                "gap": "20px",
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

        # Section 2 - Doctors Schedule
        html.Div(
            style=styles["subHeader1"],
            children=[

                # Section 2
                html.Hr(style=styles["divider2"]),
                html.H3("Doctors Schedule", style=styles["docSchedule2"]),
            ],
        ),

        # Table for Doctors Schedule List
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
                        html.Tbody(id="doctors-schedule-table-body")
                    ],
                ),
            ],
        ),
    ],
),
    ]
)

def doctor_schedule_display(app):
    # Populate dropdown options on app start
    @app.callback(
        [Output("doctor-full-name", "options"),
         Output("specialization-name", "options")],
        Input("interval-refresh", "n_intervals")
    )
    def update_dropdown_options(n_intervals):
        # Fetch distinct dropdown options from the database
        doctors = fetch_data()
        doctor_name_options = [{'label': name, 'value': name} for name in sorted(set(doctor[1] for doctor in doctors))]
        specialization_options = [{'label': spec, 'value': spec} for spec in sorted(set(doctor[2] for doctor in doctors))]
        return doctor_name_options, specialization_options

    # Callback to update the table body with filtered data
    @app.callback(
        Output("doctors-schedule-table-body", "children"),
        [
            Input("interval-refresh", "n_intervals"),  # Trigger on interval updates
            Input("doctor-full-name", "value"),  # Selected doctor full name
            Input("specialization-name", "value")  # Selected specialization type
        ]
    )
    def update_table(n_intervals, selected_doctor, selected_specialization):
        # Fetch data from the database
        doctors = fetch_data()

        # Filter data based on selected dropdown values
        if selected_doctor:
            doctors = [doctor for doctor in doctors if selected_doctor.lower() in doctor[1].lower()]
        if selected_specialization:
            doctors = [doctor for doctor in doctors if selected_specialization.lower() in doctor[2].lower()]

        if not doctors:
            # Return a message if no data matches the filters
            return [html.Tr([html.Td("No data available", colSpan=7, style={
                "text-align": "center", "padding": "10px", "border": "1px solid black"})])]

        # Generate table rows dynamically
        return [
            html.Tr(
                children=[
                    html.Td(doctor_id, style={"text-align": "center", "padding": "10px", "border": "1px solid black"}),
                    html.Td(doctor_name, style={"text-align": "center", "padding": "10px", "border": "1px solid black"}),
                    html.Td(doctor_specialization, style={"text-align": "center", "padding": "10px", "border": "1px solid black"}),
                    html.Td(doctor_availability_date, style={"text-align": "center", "padding": "10px", "border": "1px solid black"}),
                    html.Td(start_time, style={"text-align": "center", "padding": "10px", "border": "1px solid black"}),
                    html.Td(end_time, style={"text-align": "center", "padding": "10px", "border": "1px solid black"}),
                    html.Td(
                        dcc.Link(
                            html.Button(
                                "Edit", 
                                id=f"edit-{doctor_id}", 
                                style={
                                    "padding": "1px 30px", "background-color": "#b0c5ff", "color": "#05066d", 
                                    "border-radius": "5px", "border": "none"
                                }
                            ),
                            href=f"/edit_doctor?doctor_id={doctor_id}",  # Replace with your target page link
                        ),
                        style={"text-align": "center", "padding": "10px", "border": "1px solid black"}
                    ),
                ],
                style={"border": "none"}
            )
            for doctor_id, doctor_name, doctor_specialization, doctor_availability_date, start_time, end_time in doctors
        ]
