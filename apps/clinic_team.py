from dash import Dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output
from apps.dbconnect import create_connection, close_connection

# Function to fetch data from the database
def fetch_data():
    connection = create_connection()
    
    try:
        query = """
        SELECT secretary_name, secretary_email, secretary_role
        FROM clinic_secretary;
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

# Table Headers
headers = ["Employee Name", "Email Address", "Role"]

# Define styles for the layout
styles = {
    "subHeader1": {
        "padding": "40px",
        "marginLeft": "60px"
    },
    "clinic": {
        "fontSize": "18px",
        "color": "#05066d",
        "marginTop": "-25px",
        "marginBottom": "50px",
    },
    "titleClinic": {
        "fontSize": "30px",
        "color": "#05066d",
        "fontWeight": "bold",
        "marginBottom": "5px"
    },
    "divider1": {
        "width": "93%",
        "border": "2px solid #05066d",
        "marginTop": "-3px",
        "marginLeft": "-0px"
    },
    "divider2": {
        "width": "93%",
        "border": "2px solid #05066d",
        "marginTop": "-55px",
        "marginLeft": "-0px"
    },
    "employeeList": {
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
                html.H2("Clinic Team", style=styles["titleClinic"]),
                html.Hr(style=styles["divider1"]),
                dcc.Link(
                    html.Button(
                        'Add New Employee',
                        id='add-employee-button',
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
                    href='/add_employee'  # Link destination
                ),
            ],
        ),

        # The table box
        html.Div(
            style={"padding": "20px", "margin-top": "-60px"},
            children=[
                # Employee data
                html.Div(
                    style={"padding": "20px"},
                    children=[
                        # Table Container with smaller width
                        html.Table(
                            style={
                                "width": "89%",  # Reduced table width
                                "margin-left": "60px",  # Move the table to the left
                                "border": "1px solid black",
                                "border-collapse": "collapse"
                            },
                            children=[
                                # Table Header Row
                                html.Tr(
                                    children=[
                                        html.Th(
                                            children=["Search Employee"],
                                            style={
                                                "padding": "10px",
                                                "text-align": "left",
                                                "font-weight": "bold",
                                                "background-color": "#05066d",
                                                "color": "white"
                                            },
                                        ),
                                    ],
                                ),
                                # Table Body Row 
                                html.Tr(
                                    style={"border": "1px solid black"},
                                    children=[
                                        html.Td(
                                            children=[
                                                # Employee Name Input
                                                html.Div(
                                                    children=[
                                                        "Employee Name",
                                                        html.Br(),  # Line break
                                                        dcc.Input(
                                                            id="employee-name-input",  # ID for the input field
                                                            type="text",  # Type of the input field (text)
                                                            placeholder="Juan Dela Cruz",  # Placeholder text for the input
                                                            style={"width": "350px", "padding": "5px", "margin-right": "90px", "font-style": "italic"}
                                                        ),
                                                    ],
                                                    style={"text-align": "left", "color": "#05066d", "padding-left": "20px", "font-weight": "bold", "margin-right": "10px"},  # Align label and input field
                                                ),

                                                # Employee Role Input
                                                html.Div(
                                                    children=[
                                                        "Employee Role",
                                                        html.Br(),  # Line break
                                                        dcc.Input(
                                                            id="role-input",  # ID for the input field
                                                            type="text",  # Type of the input field (number)
                                                            placeholder="Enter role",  # Placeholder text for the input
                                                            style={"width": "350px", "padding": "5px", "font-style": "italic"}  # Reduced size for inline display
                                                        ),
                                                    ],
                                                    style={"text-align": "left", "color": "#05066d", "padding-bottom": "20px", "font-weight": "bold", "margin-left": "10px"},  # Align label and input field
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

        # Content 2
        html.Div(
            style=styles["subHeader1"],
            children=[

                # Section 2
                html.Hr(style=styles["divider2"]),
                html.H3("Employee", style=styles["employeeList"]),
            ],
        ),

        # Table for Secretary Information List
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
                        html.Tbody(id="clinic-team-table-body")
                    ],
                ),
            ],
        ),
    ],
),
    ]
)

def clinic_employee_display(app):
    # Callback to update the table body with data
    @app.callback(
        Output("clinic-team-table-body", "children"),
        [
            Input("interval-refresh", "n_intervals"),  # Trigger on interval updates
            Input("employee-name-input", "value"),  # Capture Employee Name input
            Input("role-input", "value")  # Capture Role input
        ]
    )
    def update_table(n_intervals, employee_name_input, role_input):
        # Fetch data
        employees = fetch_data()

        # Filter employees based on the search values for employee name and role
        if employee_name_input:
            employees = [employee for employee in employees if employee_name_input.lower() in employee[1].lower()]
        if role_input:
            employees = [employee for employee in employees if role_input.lower() in employee[2].lower()]

        if not employees:
            # Return a message if no data is available
            return [html.Tr([html.Td("No data available", colSpan=3, style={
                "text-align": "center", "padding": "10px"})])]

        # Generate table rows
        return [
            html.Tr(
                children=[
                    html.Td(employee[0], style={"text-align": "center", "padding": "10px", "border": "1px solid black"}),
                    html.Td(employee[1], style={"text-align": "center", "padding": "10px", "border": "1px solid black"}),
                    html.Td(employee[2], style={"text-align": "center", "padding": "10px", "border": "1px solid black"}),
                ],
                style={"border": "none"}
            )
            for employee in employees
        ]