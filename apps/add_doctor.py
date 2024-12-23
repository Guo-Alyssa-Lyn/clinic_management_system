import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, State
from dash.exceptions import PreventUpdate
from apps.dbconnect import create_connection, close_connection

# Define styles for the layout
styles = {
    "subHeader1": { 
        "padding": "40px",
        "marginLeft": "60px"
    },
    "backDocSched": {
        "fontSize": "18px",   
        "color": "#05066d",
        "marginTop": "-27px",
    },
    "docSched": {
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
                                "Back to Doctors Schedule Page"
                            ],
                            href="/doctor_schedule",  # Link target
                            style={
                                **styles["backDocSched"],  # Apply existing styles
                                "text-decoration": "none",  # Remove underline
                                "color": "inherit"  # Ensure link text inherits color from parent
                            },
                        ),
                    ],
                    style={"margin-bottom": "50px"}, 
                ),
                html.P("Doctors Schedule", style=styles["docSched"]),
                html.Hr(style=styles["divider1"]),
            ],
        ),

        # The table - Add New Doctor Schedule
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
                                    children=["Add New Doctor Schedule"],
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
                                                # Doctor Full Name
                                                html.Div(
                                                    children=[
                                                        "Doctor Name",
                                                        html.Br(),
                                                        dcc.Input(
                                                            id="doc-name-input", 
                                                            type="text", 
                                                            placeholder="Juan Dela Cruz", 
                                                            style={"width": "250px", "padding": "5px", "margin-bottom": "10px", "margin-right": "30px", "font-style": "italic"}
                                                        ),
                                                    ],
                                                    style={"margin-right": "20px", "text-align": "left"},
                                                ),
                                                # Specialization
                                                html.Div(
                                                    children=[
                                                        "Specialization",
                                                        html.Br(),
                                                        dcc.Input(
                                                            id="specialization-input", 
                                                            type="text", 
                                                            placeholder="Family Medicine", 
                                                            style={"width": "250px", "padding": "5px", "margin-bottom": "10px", "margin-right": "30px", "font-style": "italic"}
                                                        ),
                                                    ],
                                                    style={"margin-right": "20px", "text-align": "left"},
                                                ),
                                            ],
                                            style={
                                                "display": "flex",
                                                "gap": "20px",
                                            },
                                        ),
                                        # Second line input fields
                                        html.Div(
                                            children=[
                                                # Days Availability
                                                html.Div(
                                                    children=[
                                                        "Days Availability",
                                                        html.Br(),
                                                        dcc.DatePickerSingle(
                                                            id="date-picker-availability",
                                                            placeholder="mm/dd/yyyy",  
                                                            display_format="MM/DD/YYYY",  
                                                            style={
                                                                "margin-right": "150px",
                                                                "margin-bottom": "10px",
                                                                "width": "100px",  
                                                            },
                                                            className="custom-date-picker"  
                                                        ),
                                                    ],
                                                    style={"margin-right": "20px", "text-align": "left"},
                                                ),
                                                # Time Availability - Start
                                                html.Div(
                                                    children=[
                                                        "Time Availability (Start)",
                                                        html.Br(),
                                                        html.Div(
                                                            children=[
                                                                dcc.Dropdown(
                                                                    id="start-hour-dropdown",
                                                                    options=[{'label': f'{i%12 if i%12 != 0 else 12}', 'value': i} for i in range(1, 13)],
                                                                    value=9,
                                                                    style={"width": "90px"}
                                                                ),
                                                                dcc.Dropdown(
                                                                    id="start-minute-dropdown",
                                                                    options=[{'label': f'{i:02d}', 'value': f'{i:02d}'} for i in range(0, 60, 5)],
                                                                    value="00",
                                                                    style={"width": "80px"}
                                                                ),
                                                                dcc.Dropdown(
                                                                    id="start-ampm-dropdown",
                                                                    options=[{'label': 'AM', 'value': 'AM'}, {'label': 'PM', 'value': 'PM'}],
                                                                    value='AM',
                                                                    style={"width": "80px"}
                                                                ),
                                                            ],
                                                            style={"display": "flex", "gap": "10px", "text-align": "left"},
                                                        ),
                                                    ],
                                                    style={"flex-direction": "column", "display": "flex", "gap": "5px", "text-align": "left", "margin-left": "30px"},
                                                ),
                                                # Time Availability - End
                                                html.Div(
                                                    children=[
                                                        "Time Availability (End)",
                                                        html.Br(),
                                                        html.Div(
                                                            children=[
                                                                dcc.Dropdown(
                                                                    id="end-hour-dropdown",
                                                                    options=[{'label': f'{i%12 if i%12 != 0 else 12}', 'value': i} for i in range(1, 13)],
                                                                    value=5,
                                                                    style={"width": "90px"}
                                                                ),
                                                                dcc.Dropdown(
                                                                    id="end-minute-dropdown",
                                                                    options=[{'label': f'{i:02d}', 'value': f'{i:02d}'} for i in range(0, 60, 5)],
                                                                    value="00",
                                                                    style={"width": "80px"}
                                                                ),
                                                                dcc.Dropdown(
                                                                    id="end-ampm-dropdown",
                                                                    options=[{'label': 'AM', 'value': 'AM'}, {'label': 'PM', 'value': 'PM'}],
                                                                    value='PM',
                                                                    style={"width": "80px"}
                                                                ),
                                                            ],
                                                            style={"display": "flex", "gap": "10px", "text-align": "left"},
                                                        ),
                                                    ],
                                                    style={"flex-direction": "column", "display": "flex", "gap": "5px", "text-align": "left", "margin-left": "50px"},
                                                ),
                                            ],
                                            style={
                                                "display": "flex",
                                                "gap": "20px",
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
                                                                "font-size": "14px",
                                                                "font-weight": "bold",
                                                                "padding": "5px 40px", 
                                                                "border-radius": "5px",
                                                                "margin-right": "20px", 
                                                                "margin-top": "40px", 
                                                                "border": "none", 
                                                                "cursor": "pointer"
                                                            }
                                                        ),
                                                        href="/doctor_schedule",  # Replace with the target URL
                                                    ),
                                                html.Button(
                                                    "Add",
                                                    id="add-button", 
                                                    n_clicks=0,
                                                    style={
                                                        "background-color": "#4CAF50", 
                                                        "color": "white", 
                                                        "border-radius": "5px",
                                                        "font-size": "14px",
                                                        "font-weight": "bold",
                                                        "padding": "5px 45px",  
                                                        "margin-top": "40px", 
                                                        "border": "none", 
                                                        "cursor": "pointer"
                                                    }
                                                ),
                                            ],
                                            style={
                                                "margin-top": "10px", 
                                                "text-align": "right",  
                                                "width": "100%",  
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
                                        "margin": "15px"
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
        html.Div(id="submit-success", style={"margin-top": "20px"}),
    ]
)

def register_callbacks(app):
    # Callback to add doctor information to the database
    @app.callback(
        Output("submit-success", "children"),
        Input("add-button", "n_clicks"),
        [
            State("doc-name-input", "value"),
            State("specialization-input", "value"),
            State("date-picker-availability", "date"),
            State("start-hour-dropdown", "value"),
            State("start-minute-dropdown", "value"),
            State("start-ampm-dropdown", "value"),
            State("end-hour-dropdown", "value"),
            State("end-minute-dropdown", "value"),
            State("end-ampm-dropdown", "value")
        ],
    )
    def add_doctor(n_clicks, doctor_name, doctor_specialization, date_availability, start_hour, start_minute, start_ampm, end_hour, end_minute, end_ampm):
        if not n_clicks or n_clicks == 0:
            raise PreventUpdate

        if not all([doctor_name, doctor_specialization, date_availability, start_hour, start_minute, start_ampm, end_hour, end_minute, end_ampm]):
            return "Please fill in all fields."

        start_time = f"{start_hour}:{start_minute} {start_ampm}"
        end_time = f"{end_hour}:{end_minute} {end_ampm}"

        doctor_availability_time = f"{start_time} - {end_time}"

        query = """
        INSERT INTO doctor (doctor_name, doctor_specialization, doctor_availability_date, doctor_availability_time)
        VALUES (%s, %s, %s, %s)
        """
        data = (doctor_name, doctor_specialization, date_availability, doctor_availability_time)

        connection = create_connection()
        if not connection:
            return "Database connection failed."

        try:
            cursor = connection.cursor()
            cursor.execute(query, data)
            connection.commit()

            # Return the success message with fading effect
            return html.Div(
                "New doctor schedule added successfully!",
                id="success-message",
                style={
                    "backgroundColor": "#28a745",  # Green background
                    "color": "white",  # White text
                    "padding": "10px",  # Padding for spacing
                    "borderRadius": "5px",  # Rounded corners
                    "textAlign": "center",  # Centered text
                    "transition": "opacity 2s ease-out",  # Smooth transition effect
                    "opacity": 1,  # Full opacity initially
                }
            )
        except Exception as e:
            return f"An error occurred: {e}"
        finally:
            close_connection(connection)
            
    def patients_page_layout():
        return html.Div([
            dcc.Location(id="url", refresh=False),
            html.Div(id="submit-success"),  # Placeholder for error/success messages
            html.Div(id="success-message"),  # Success message will go here
            html.Div(id="patient-list"),
        ])