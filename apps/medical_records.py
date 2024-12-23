import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Output, Input
from dash.exceptions import PreventUpdate
from apps.dbconnect import create_connection, close_connection

import pandas as pd

# Function to fetch data from the database
def fetch_data():
    connection = create_connection()
    
    try:
        query = """
        SELECT patient_id, patient_first_name, patient_last_name
        FROM patient;
        """
        
        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    
    except Exception as e:
        print(f"Error: {e}")
        return []
    
    finally:
        cursor.close()
        close_connection(connection)

headers = ["ID", "Patient First Name", "Patient Last Name", "View", "Edit"]

# Define styles for the layout
styles = {
    "subHeader1": {
        "padding": "40px",
        "marginLeft": "60px"
    },
    "medRecords": {
        "fontSize": "18px",
        "color": "#05066d",
        "marginBottom": "50px",
    },
    "titleMedRecords": {
        "fontSize": "30px",
        "color": "#05066d",
        "fontWeight": "bold"
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
    "patientMedRecords": {
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
                # Section 1
                html.P(
                    children=[
                        "Patient / ",  # Normal text
                        html.Span(
                            "Medical Records",  # Text to make bold and underlined
                            style={
                                "fontWeight": "bold",  # Bold text
                                "textDecoration": "underline",  # Underlined text
                            },
                        ),
                    ],
                    style=styles["medRecords"],
                ),
                html.H2("Medical Records", style=styles["titleMedRecords"]),
                html.Hr(style=styles["divider1"]),
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
                        "border-collapse": "collapse",
                    },
                    children=[
                        # Table Header Row
                        html.Tr(
                            children=[
                                html.Th(
                                    children=["Search Patient Name"],
                                    style={
                                        "padding": "10px",
                                        "text-align": "left",
                                        "font-weight": "bold",
                                        "background-color": "#05066d",
                                        "color": "white",
                                    },
                                )
                            ]
                        ),
                        # Table Body Row
                        html.Tr(
                            style={"border": "1px solid black"},
                            children=[
                                html.Td(
                                    children=[
                                        # First Name Input
                                        html.Div(
                                            children=[
                                                "Patient First Name",
                                                html.Br(),  # Line break
                                                dcc.Input(
                                                    id="first-name-input",  # ID for the input field
                                                    type="text",  # Type of the input field (text)
                                                    placeholder="Juan",  # Placeholder text for the input
                                                    style={
                                                        "width": "350px",
                                                        "padding": "5px",
                                                        "font-style": "italic",
                                                    }  # Reduced size for inline display
                                                ),
                                            ],
                                            style={
                                                "text-align": "left",
                                                "color": "#05066d",
                                                "font-weight": "bold",
                                                "margin-right": "10px"
                                            },  # Align label and input field
                                        ),
                                        # Last Name Input
                                        html.Div(
                                            children=[
                                                "Patient Last Name",
                                                html.Br(),  # Line break
                                                dcc.Input(
                                                    id="last-name-input",  # ID for the input field
                                                    type="text",  # Type of the input field (text)
                                                    placeholder="Dela Cruz",  # Placeholder text for the input
                                                    style={
                                                        "width": "350px",
                                                        "padding": "5px",
                                                        "font-style": "italic",
                                                    }  # Reduced size for inline display
                                                ),
                                            ],
                                            style={
                                                "text-align": "left",
                                                "color": "#05066d",
                                                "font-weight": "bold",
                                                "margin-left": "10px"
                                            },  # Align label and input field
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
                            ]
                        ),
                    ]
                ),
                # Data table for filtered results
                html.Div(id="patient-table")
            ],
        ),
    ]
),

        # Content 2
        html.Div(
            style=styles["subHeader1"],
            children=[
                
                # Section 2
                html.Hr(style=styles["divider2"]),
                html.H3("Patient Medical Records", style=styles["patientMedRecords"]),
            ],
        ),

        # Table for Patient Medical Record List
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
                        html.Tbody(id="medical-record-table-body")
                    ],
                ),
            ],
        ),
    ],
),
    ]
)

def medical_records_display(app):
    @app.callback(
        Output("medical-record-table-body", "children"),
        [Input("interval-refresh", "n_intervals"),
         Input("first-name-input", "value"),
         Input("last-name-input", "value")]
    )
    def update_table(n_intervals, first_name_input, last_name_input):
        # Fetch data
        patients = fetch_data()

        # Filter patients based on first name and last name
        if first_name_input:
            patients = [patient for patient in patients if first_name_input.lower() in patient[1].lower()]
        if last_name_input:
            patients = [patient for patient in patients if last_name_input.lower() in patient[2].lower()]

        if not patients:
            # Return a message if no data is available
            return [html.Tr([html.Td("No data available", colSpan=len(headers), style={"text-align": "center", "padding": "10px"})])]

        # Generate table rows 
        return [
            html.Tr(
                children=[
                    html.Td(patient_id, style={"text-align": "center", "padding": "10px", "border": "1px solid black"}),
                    html.Td(first_name, style={"text-align": "center", "padding": "10px", "border": "1px solid black"}),
                    html.Td(last_name, style={"text-align": "center", "padding": "10px", "border": "1px solid black"}),
                    html.Td(
                        html.A(
                            html.Button("View", id=f"view-{patient_id}", style={
                                "padding": "1px 30px", 
                                "background-color": "#05066d", 
                                "color": "white", 
                                "border-radius": "5px", 
                                "border": "none"}),
                            href=f"/view_patient_medical_records/{patient_id}",  # Dynamic link based on patient_id
                            style={"text-decoration": "none"}
                        ),
                        style={"text-align": "center", "padding": "10px", "border": "1px solid black"}
                    ),
                    html.Td(
                        html.A(
                            "Edit", 
                            href=f"/edit_medical_records?patient_id={patient_id}",
                            id=f"edit-{patient_id}", 
                            style={
                                "padding": "1px 30px", 
                                "background-color": "#b0c5ff", 
                                "color": "#05066d", 
                                "border-radius": "5px", 
                                "border": "none", 
                                "text-decoration": "none"
                            }
                        ),
                        style={"text-align": "center", "padding": "10px", "border": "1px solid black"}
                    ),
                ],
                style={"border": "none"}
            )
            for patient_id, first_name, last_name in patients
        ]