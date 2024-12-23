import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.exceptions import PreventUpdate
import datetime
import calendar
from dash import html, Output, Input
from dash import dcc
from apps.dbconnect import create_connection, close_connection

# Function to fetch doctor's availability based on the selected date
def get_doctor_availability(selected_date):
    try:
        # Use the create_connection function to get a connection to the database
        connection = create_connection()
        if connection is None:
            return "Error connecting to the database"

        cursor = connection.cursor(dictionary=True)
        
        # Query to fetch doctor availability based on selected date
        query = """
            SELECT doctor_name, doctor_specialization, doctor_availability_time
            FROM doctor
            WHERE doctor_availability_date = %s
        """
        cursor.execute(query, (selected_date,))
        result = cursor.fetchall()

        # Close the connection after the query
        close_connection(connection)

        # Return result
        if result:
            return result
        else:
            return "No results"

    except Exception as err:
        print(f"Error: {err}")
        return "Error fetching data"

# Function to fetch patient appointments based on the selected date
def get_patient_appointments(selected_date):
    try:
        # Use the create_connection function to get a connection to the database
        connection = create_connection()
        if connection is None:
            return "Error connecting to the database"

        cursor = connection.cursor(dictionary=True)
        
        # Query to fetch patient and appointment details for the selected date
        query = """
            SELECT p.patient_first_name, p.patient_last_name, a.appointment_date, a.appointment_time
            FROM patient p
            JOIN appointment a ON p.patient_id = a.patient_id
            WHERE a.appointment_date = %s
        """
        cursor.execute(query, (selected_date,))
        result = cursor.fetchall()

        # Close the connection after the query
        close_connection(connection)

        # Return result
        if result:
            return result
        else:
            return "No results"

    except Exception as err:
        print(f"Error: {err}")
        return "Error fetching data"

# Function to fetch patient appointments based on the selected date
def get_counted_status_waiting(status):
    try:
        # Use the create_connection function to get a connection to the database
        connection = create_connection()
        if connection is None:
            return "Error connecting to the database"

        cursor = connection.cursor(dictionary=True)
        
        # Query to fetch appointments based on the provided status
        query = """
            SELECT appointment_status
            FROM appointment
            WHERE appointment_status = %s
        """
        cursor.execute(query, (status,))
        result = cursor.fetchall()

        return result if result else []

    except Exception as err:
        print(f"Error: {err}")
        return "Error fetching data"

    finally:
        # Ensure the connection is closed
        if connection:
            close_connection(connection)

# Function to fetch patient appointments based on the selected date
def get_counted_status_served(status):
    try:
        # Use the create_connection function to get a connection to the database
        connection = create_connection()
        if connection is None:
            return "Error connecting to the database"

        cursor = connection.cursor(dictionary=True)
        
        # Query to fetch appointments based on the provided status
        query = """
            SELECT appointment_status
            FROM appointment
            WHERE appointment_status = %s
        """
        cursor.execute(query, (status,))
        result = cursor.fetchall()

        return result if result else []

    except Exception as err:
        print(f"Error: {err}")
        return "Error fetching data"

    finally:
        # Ensure the connection is closed
        if connection:
            close_connection(connection)

# Define styles for the layout
styles = {
    "subHeader1": {
        "padding": "40px",
        "marginLeft": "60px"
    },
    "homePage": {
        "fontWeight": "bold",
        "fontSize": "30px",
        "color": "#05066d",
    },
    "divider1": {
        "width": "93%",
        "border": "2px solid #05066d",
    },
    "dailyDashboard": {
        "fontSize": "18px",
        "color": "#05066d",
        "marginBottom": "-60px",
    },
    "divider2": {
        "marginTop": "190px",
        "width": "93%",
        "border": "2px solid #05066d"
    },
    "divider3": {
        "marginTop": "190px",
        "width": "93%",
        "border": "2px solid #05066d"
    },
    "calendar": {
        "fontSize": "18px",
        "color": "#05066d",
        "marginBottom": "-40px",
    },
    "dailySchedChecker": {
        "fontSize": "18px",
        "color": "#05066d",
        "marginBottom": "-40px",
    },
}

# Set up routing and layout
layout = html.Div(
    children=[

        dcc.Interval(
        id="interval-component-status",
        interval=10*1000,  # Update every 10 seconds
        n_intervals=0
    ),

        # Content 
        html.Div(
            style=styles["subHeader1"],
            children=[
                # Section 1
                html.H2("Home Page", style=styles["homePage"]),
                html.Hr(style=styles["divider1"]),
                html.H3("Daily Dashboard", style=styles["dailyDashboard"]),
            ],
        ),

    # The number of patients
    html.Div(
    style={
        "display": "flex",  # Flexbox layout
        "gap": "30px",  # Space between the two elements
        "align-items": "flex-start",  # Align items at the top (start)
        "padding": "20px",  # Optional padding for the parent container
        "width": "50%",  # Make the parent container 85% of the width
        "margin": "0 auto",  # Center the parent container
        "margin-bottom": "-250px", 

    },
    children=[
        # The patients waiting in line

        html.Div(
            style={"flex": "1", "padding": "20px"},  # Use flex for equal width
            children=[
                html.Table(
                    style={
                        "width": "100%",  # Full width of the container
                        "border": "1px solid black",
                        "border-collapse": "collapse",
                    },

                    children=[
                        html.Tr(
                            children=[
                                html.Th(
                                    children=[
                                        "Patients Waiting in Line",
                                    ],
                                    style={
                                        "padding": "20px",
                                        "text-align": "center",
                                        "font-weight": "bold",
                                        "background-color": "#05066d",
                                        "color": "white",
                                    },
                                )
                            ],
                        ),

                        html.Tr(
                            style={"border": "1px solid black"},
                            children=[
                                html.Td(
                                        html.Div(id="patients-waiting", children=""),
                                    style={
                                        "padding": "20px",
                                        "text-align": "center",
                                        "background-color": "#f9f9f9",
                                    },
                                )
                            ],
                        ),
                    ],
                ),
            ],
        ),

        # The served patients
        html.Div(
            style={"flex": "1", "padding": "20px"},  # Use flex for equal width
            children=[
                html.Table(
                    style={
                        "width": "100%",  # Full width of the container
                        "border": "1px solid black",
                        "border-collapse": "collapse",
                    },
                    children=[
                        html.Tr(
                            children=[
                                html.Th(
                                    children=[
                                        "Patient Served",
                                    ],
                                    style={
                                        "padding": "20px",
                                        "text-align": "center",
                                        "font-weight": "bold",
                                        "background-color": "#05066d",
                                        "color": "white",
                                    },
                                )
                            ],
                        ),
                        html.Tr(
                            style={"border": "1px solid black"},
                            children=[
                                html.Td(
                                        html.Div(id="patients-served", children=""),
                                    style={
                                        "padding": "20px",
                                        "text-align": "center",
                                        "background-color": "#f9f9f9",
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



        # Content 
        html.Div(
            style=styles["subHeader1"],
            children=[
                # Section 2
                html.Hr(style=styles["divider2"]),
                html.H3("Daily Schedule Checker", style=styles["dailySchedChecker"]),
            ],
        ),

    html.Div(
    style={
        "display": "flex",  # Flexbox layout
        "gap": "30px",  # Space between the two elements
        "align-items": "flex-start",  # Align items at the top (start)
        "padding": "20px",  # Optional padding for the parent container
        "width": "80%",  # Make the parent container 85% of the width
        "margin": "0 auto",  # Center the parent container
        "margin-bottom": "-250px",
    },
    children=[
        # The Appointment Checker box
        html.Div(
            style={"flex": "1", "padding": "20px"},  # Use flex for equal width
            children=[
                html.Table(
                    style={
                        "width": "100%",  # Full width of the container
                        "border": "1px solid black",
                        "border-collapse": "collapse",
                    },
                    children=[
                        html.Tr(
                            children=[
                                html.Th(
                                    children=[
                                        "Appointment Checker",
                                        html.Br(),
                                        html.Div(
                                            "Please select the appointment schedule date that you would like to check.",
                                            style={
                                                "font-weight": "normal",
                                                "font-size": "13px",
                                                "color": "white",
                                                "font-style": "italic",
                                            },
                                        ),
                                    ],
                                    style={
                                        "padding": "10px",
                                        "text-align": "left",
                                        "font-weight": "bold",
                                        "background-color": "#05066d",
                                        "color": "white",
                                    },
                                )
                            ],
                        ),
                        html.Tr(
                            style={"border": "1px solid black"},
                            children=[
                                html.Td(
                                    children=[
                                        dcc.DatePickerSingle(
                                            id="date-picker-appointment-checker",
                                            placeholder="mm/dd/yyyy",
                                            display_format="MM/DD/YYYY",
                                            style={
                                                "margin-bottom": "10px",
                                                "margin-left": "60px",
                                                
                                            },
                                            className="custom-date-picker-home",
                                        ),
                                    ],
                                    style={
                                        "padding": "10px",
                                        "text-align": "left",
                                        "background-color": "#f9f9f9",
                                    },
                                )
                            ],
                        ),
                    ],
                ),
                html.Div(
                    id="appointment-checker-output",  # The ID for the callback to update
                    style={
                        "padding": "10px",
                        "margin-top": "1px",
                        "background-color": "#f9f9f9",
                        "border": "1px solid #ddd",  # Optional: to add a border around the section
                        "border-radius": "5px",  # Optional: to round the corners of the border
                    },
                    children=[]  # Initially empty; will be updated by the callback
                ),
            ], 
        ),

        # The Doctor Availability box
        html.Div(
        style={"flex": "1", "padding": "20px"},  # Use flex for equal width
        children=[
            html.Table(
                style={
                    "width": "100%",  # Full width of the container
                    "border": "1px solid black",
                    "border-collapse": "collapse",
                },
            children=[
                html.Tr(
                    children=[
                        html.Th(
                            children=[
                                "Doctor Availability",
                                html.Br(),
                                html.Div(
                                    "Please select the doctor availability date that you would like to check.",
                                    style={
                                        "font-weight": "normal",
                                        "font-size": "13px",
                                        "color": "white",
                                        "font-style": "italic",
                                    },
                                ),
                            ],
                            style={
                                "padding": "10px",
                                "text-align": "left",
                                "font-weight": "bold",
                                "background-color": "#05066d",
                                "color": "white",
                            },
                        )
                    ],
                ),
                html.Tr(
                    style={"border": "1px solid black"},
                    children=[
                        html.Td(
                            children=[
                                dcc.DatePickerSingle(
                                    id="date-doctor-availability",
                                    placeholder="mm/dd/yyyy",
                                    display_format="MM/DD/YYYY",
                                    style={
                                        "margin-bottom": "10px",
                                        "margin-left": "60px",
                                        "width": "100px",
                                    },
                                    className="custom-date-picker-home",
                                ),
                            ],
                            style={
                                "padding": "10px",
                                "text-align": "left",
                                "background-color": "#f9f9f9",
                            },
                        )
                    ],
                ),
            ],
        ),
        # Add a new Div here to display the fetched doctor's availability schedule
        html.Div(
            id="doctor-availability-output",  # The ID for the callback to update
            style={
                "padding": "10px",
                "margin-top": "1px",
                "background-color": "#f9f9f9",
                "border": "1px solid #ddd",  # Optional: to add a border around the section
                "border-radius": "5px",  # Optional: to round the corners of the border
            },
            children=[]  # Initially empty; will be updated by the callback
        ),
    ],
),
    ],
),

    ]
)


# Doctor availability callback
def home_page_functions(app):
    # Callback for Doctor Availability
    @app.callback(
        Output("doctor-availability-output", "children"),
        [Input("date-doctor-availability", "date")],
    )
    def display_doctor_availability(selected_date):
        if selected_date:
            # Convert date to the required format
            selected_date = datetime.datetime.strptime(selected_date, "%Y-%m-%d").date()  # Corrected usage

            # Fetch doctor's availability from the database
            availability = get_doctor_availability(selected_date)

            if availability == "No results":
                return html.Div("No results", style={"color": "red"})

            # If results are found, display the doctor's availability
            availability_list = [
                html.Table(
                    # Table styling
                    style={
                        "width": "100%", 
                        "border": "1px solid black", 
                        "border-collapse": "collapse", 
                        "margin-top": "0px"
                    },
                    children=[
                        html.Tr(
                            # Header row
                            children=[
                                html.Th("Doctor Name", style={"padding": "10px", "text-align": "center", "background-color": "#05066d", "color": "white"}),
                                html.Th("Specialization", style={"padding": "10px", "text-align": "center", "background-color": "#05066d", "color": "white"}),
                                html.Th("Available Time", style={"padding": "10px", "text-align": "center", "background-color": "#05066d", "color": "white"}),
                            ]
                        ),
                        # Data rows for doctor's availability
                        *[
                            html.Tr(
                                children=[
                                    html.Td(item['doctor_name'], style={"padding": "10px", "font-size": "14px", "text-align": "center", "background-color": "#f9f9f9"}),
                                    html.Td(item['doctor_specialization'], style={"padding": "10px", "font-size": "14px", "text-align": "center", "background-color": "#f9f9f9"}),
                                    html.Td(item['doctor_availability_time'], style={"padding": "10px", "font-size": "14px", "text-align": "center", "background-color": "#f9f9f9"}),
                                ]
                            ) 
                            for item in availability
                        ]
                    ]
                )
            ]

            return availability_list
        return html.Div("Please select a date", style={"color": "gray"})

    # Callback for Appointment Checker
    @app.callback(
        Output("appointment-checker-output", "children"),
        [Input("date-picker-appointment-checker", "date")],
    )
    def display_patient_appointments(selected_date):
        if selected_date:
            # Convert date to the required format
            selected_date = datetime.datetime.strptime(selected_date, "%Y-%m-%d").date()  # Corrected usage

            # Fetch patient appointment details from the database
            appointments = get_patient_appointments(selected_date)

            if appointments == "No results":
                return html.Div("No results", style={"color": "red"})

            # If results are found, display the patient appointments
            appointments_list = [
                html.Table(
                    # Table styling
                    style={
                        "width": "100%", 
                        "border": "1px solid black", 
                        "border-collapse": "collapse", 
                        "margin-top": "0px"
                    },
                    children=[
                        html.Tr(
                            # Header row
                            children=[
                                html.Th("Patient Name", style={"padding": "10px", "text-align": "center", "background-color": "#05066d", "color": "white"}),
                                html.Th("Appointment Date", style={"padding": "10px", "text-align": "center", "background-color": "#05066d", "color": "white"}),
                                html.Th("Appointment Time", style={"padding": "10px", "text-align": "center", "background-color": "#05066d", "color": "white"}),
                            ]
                        ),
                        # Data rows for patient appointments
                        *[
                            html.Tr(
                                children=[
                                    html.Td(f"{item['patient_first_name']} {item['patient_last_name']}", style={"padding": "10px", "font-size": "14px", "text-align": "center", "background-color": "#f9f9f9"}),
                                    html.Td(item['appointment_date'], style={"padding": "10px", "font-size": "14px", "text-align": "center", "background-color": "#f9f9f9"}),
                                    html.Td(item['appointment_time'], style={"padding": "10px", "font-size": "14px", "text-align": "center", "background-color": "#f9f9f9"}),
                                ]
                            ) 
                            for item in appointments
                        ]
                    ]
                )
            ]

            return appointments_list
        return html.Div("Please select a date", style={"color": "gray"})
    
    @app.callback(
    [Output("patients-waiting", "children"),
     Output("patients-served", "children")],
    [Input("interval-component-status", "n_intervals")]
    )
    def update_patient_counts(n_intervals):
        try:
            waiting_results = get_counted_status_waiting("Waiting In Line")
            served_results = get_counted_status_served("Served")

            waiting_count = len(waiting_results) if isinstance(waiting_results, list) else 0
            served_count = len(served_results) if isinstance(served_results, list) else 0

            return str(waiting_count), str(served_count)
        except Exception as e:
            print(f"Error updating counts: {e}")
            return "Error", "Error"