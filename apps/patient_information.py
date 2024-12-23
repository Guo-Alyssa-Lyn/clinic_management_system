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
        SELECT patient_id, patient_first_name, patient_middle_name, patient_last_name,
               patient_birthday, patient_sex, patient_contact_number
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

headers = ["ID", "Name", "Birthday", "Sex", "Contact", "View", "Edit"]

# Define styles for the layout
styles = {
    "subHeader1": {
        "padding": "40px",
        "marginLeft": "60px"
    },
    "patientInfo": {
        "fontSize": "18px",
        "color": "#05066d",
        "marginTop": "-25px",
        "marginBottom": "50px",
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
    "divider2": {
        "width": "93%",
        "border": "2px solid #05066d",
        "marginTop": "-55px"
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
                # Section 1
                html.P(
                    children=[
                        "Patient / ",  # Normal text
                        html.Span(
                            "Patient Information",  # Text to make bold and underlined
                            style={
                                "fontWeight": "bold",  # Bold text
                                "textDecoration": "underline",  # Underlined text
                            },
                        ),
                    ],
                    style=styles["patientInfo"],
                ),
                html.H2("Patient Information", style=styles["titlePatientInfo"]),
                html.Hr(style=styles["divider1"]),
                dcc.Link(
                    html.Button(
                        'Add New Patient',
                        id='add-patient-button',
                        n_clicks=0,
                        style={
                            'backgroundColor': '#b0c5ff',  # Button background color
                            'color': '#05066d',  # Text color
                            'fontSize': '14px',  # Font size
                            'fontWeight': 'bold',  # Bold text
                            'padding': '5px 30px',  # Padding around text
                            'border': '1px solid',  # Border
                            'borderRadius': '5px',  # Rounded corners
                            'cursor': 'pointer',  # Pointer cursor on hover
                            'boxShadow': '0px 4px 6px rgba(0, 0, 0, 0.1)',  # Shadow effect
                            'transition': 'background-color 0.3s ease',  # Smooth hover effect
                        },
                    ),
                    href='/add_new_patient'  # Link destination
                ),
            ],
        ),

        # The table box
        html.Div(
    style={"padding": "20px", "margin-top": "-60px"},
    children=[
        # The Table Box with Search Bar
        html.Div(
            style={"padding": "20px", "margin-top": "-10px", "margin-left": "-20px"},
            children=[
                html.Div(
                    style={"padding": "20px"},
                    children=[
                        # Table Container with smaller width
                        html.Table(
                            style={
                                "width": "89%",  # Reduced table width
                                "margin-left": "60px",  # Move the table to the left
                                "border": "1px solid black",
                                "border-collapse": "collapse",
                            },
                            children=[
                                # Table Header Row for Search Bar
                                html.Tr(
                                    children=[
                                        html.Th(
                                            children=["Search Patient"],
                                            style={
                                                "padding": "10px",
                                                "text-align": "left",
                                                "font-weight": "bold",
                                                "background-color": "#05066d",
                                                "color": "white",
                                            },
                                        ),
                                    ],
                                ),
                                # Table Body Row for Search Input
                                html.Tr(
                                    style={"border": "1px solid black"},
                                    children=[
                                        html.Td(
                                            children=[
                                                # Search Bar Section
                                                html.Div(
                                                    children=[
                                                        "Patient Name",
                                                        html.Br(),  # Line break
                                                        dcc.Input(
                                                            id="search-bar-patient",  # ID for the input field
                                                            type="text",  # Type of the input field (text)
                                                            placeholder="Juan Dela Cruz",  # Placeholder text for the input
                                                            style={
                                                                "width": "350px",
                                                                "padding": "5px",
                                                                "margin-right": "90px",
                                                                "font-style": "italic",
                                                            },
                                                        ),
                                                    ],
                                                    style={
                                                        "text-align": "left",
                                                        "color": "#05066d",
                                                        "padding-left": "20px",
                                                        "font-weight": "bold",
                                                        "margin-right": "10px",
                                                    },  # Align label and input field
                                                ),
                                            ],
                                            style={
                                                "padding": "10px",
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
    ]
),

        # Content 2
        html.Div(
            style=styles["subHeader1"],
            children=[

                # Section 2
                html.Hr(style=styles["divider2"]),
                html.H3("Patient Records", style=styles["patientRecords"]),
            ],
        ),

        # Assuming `data` is already fetched and formatted
        # Patient Information Table
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
                        html.Tbody(id="patient-table-body")
                    ],
                ),
            ],
        ),
    ],
),
    ]
)

def update_table_display(app):
    # Callback to update the table body with data
    @app.callback(
        Output("patient-table-body", "children"),
        [Input("interval-refresh", "n_intervals"),  # Trigger on interval updates
         Input("search-bar-patient", "value")]  # Capture search bar input
    )
    def update_table(n_intervals, search_value):
        # Fetch data
        patients = fetch_data()

        # Filter patients based on the search value (if provided)
        if search_value:
            patients = [
                patient for patient in patients
                if search_value.lower() in f"{patient[1]} {patient[2]} {patient[3]}".lower()
            ]

        if not patients:
            # Return a message if no data is available
            return [html.Tr([html.Td("No data available", colSpan=len(headers), style={
                "text-align": "center", "padding": "10px"})])]

        # Generate table rows
        return [
            html.Tr(
                children=[
                    html.Td(patient_id, style={"text-align": "center", "padding": "10px", "border": "1px solid black"}),
                    html.Td(f"{first_name} {middle_name} {last_name}", style={"text-align": "center", "padding": "10px", "border": "1px solid black"}),
                    html.Td(birthday, style={"text-align": "center", "padding": "10px", "border": "1px solid black"}),
                    html.Td(sex, style={"text-align": "center", "padding": "10px", "border": "1px solid black"}),
                    html.Td(contact, style={"text-align": "center", "padding": "10px", "border": "1px solid black"}),
                    html.Td(
                            dcc.Link(
                                html.Button(
                                    "View",
                                    style={
                                        "padding": "1px 30px",  # Adjust padding as in the first block
                                        "background-color": "#05066d",  # Use the same background color
                                        "color": "white",  # Change text color to white
                                        "border-radius": "5px",  # Apply rounded corners
                                        "border": "none",  # Remove border
                                    },
                                ),
                                href=f"/view_patient_information?patient_id={patient_id}",  # Pass the patient_id via the URL
                            ),
                            style={
                                "text-align": "center",  # Center text
                                "padding": "10px",  # Adjust padding as in the first block
                                "border": "1px solid black",  # Add border
                            },
                        ),
                    html.Td(
                            dcc.Link(
                                html.Button(
                                    "Edit",
                                    style={
                                        "padding": "1px 30px",  # Adjust padding as in the first block
                                        "background-color": "#b0c5ff",  # Use the same background color
                                        "color": "#05066d",  # Change text color to white
                                        "border-radius": "5px",  # Apply rounded corners
                                        "border": "none",  # Remove border
                                    },
                                ),
                                href=f"/edit_patient_information?patient_id={patient_id}",  # Pass the patient_id via the URL
                            ),
                            style={
                                "text-align": "center",  # Center text
                                "padding": "10px",  # Adjust padding as in the first block
                                "border": "1px solid black",  # Add border
                            },
                        ),
                ],
                style={"border": "none"}
            )
            for patient_id, first_name, middle_name, last_name, birthday, sex, contact in patients
        ]