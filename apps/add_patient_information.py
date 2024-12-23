import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, State
from dash.exceptions import PreventUpdate
from apps.dbconnect import create_connection, close_connection

# Define styles for the layout
styles = {
    "subHeader1": {"padding": "40px", "marginLeft": "60px"},
    "backPatientInfo": {"fontSize": "18px", "marginTop": "-30px", "color": "#05066d"},
    "patientInfo": {"fontSize": "30px", "color": "#05066d"},
    "divider1": {"marginTop": "-3px", "width": "93%", "border": "2px solid #05066d"},
}

# Layout for adding new patient
layout = html.Div(
    children=[
        html.Div(
            style=styles["subHeader1"],
            children=[
                html.Div(
                    children=[
                        html.A(
                            [
                                html.Img(
                                    src="/assets/resources/Arrow Icon.png",
                                    style={
                                        "width": "20px",
                                        "height": "20px",
                                        "margin-right": "8px",
                                        "margin-bottom": "3px",
                                        "vertical-align": "middle",
                                    },
                                ),
                                "Back to Patient Information Page",
                            ],
                            href="/patient_information",
                            style={**styles["backPatientInfo"], "text-decoration": "none", "color": "inherit"},
                        ),
                    ],
                    style={"margin-bottom": "50px"},
                ),
                html.H2("Patient Information", style=styles["patientInfo"]),
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
                                        "Add New Patient",
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
                                                        "Patient First Name",
                                                        html.Br(),  # Line break
                                                        dcc.Input(
                                                            id="first-name-input",  # ID for the input field
                                                            type="text",  # Type of the input field (text)
                                                            placeholder="Juan",  # Placeholder text for the input
                                                            style={"width": "250px", "padding": "5px", "margin-bottom": "10px", "font-style": "italic"}  # Input style
                                                        ),
                                                    ],
                                                    style={"margin-right": "20px", "text-align": "left"},  # Spacing and alignment
                                                ),

                                                # Patient Middle Name
                                                html.Div(
                                                    children=[
                                                        "Patient Middle Name",
                                                        html.Br(),  # Line break
                                                        dcc.Input(
                                                            id="middle-name-input",  # ID for the input field
                                                            type="text",  # Type of the input field (text)
                                                            placeholder="Antonio",  # Placeholder text for the input
                                                            style={"width": "250px", "padding": "5px", "margin-bottom": "10px", "font-style": "italic"}  # Input style
                                                        ),
                                                    ],
                                                    style={"margin-right": "20px", "text-align": "left"},  # Spacing and alignment
                                                ),
                                                # Patient Last Name
                                                html.Div(
                                                    children=[
                                                        "Patient Last Name",
                                                        html.Br(),  # Line break
                                                        dcc.Input(
                                                            id="last-name-input",  # ID for the input field
                                                            type="text",  # Type of the input field (text)
                                                            placeholder="Dela Cruz",  # Placeholder text for the input
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

                                        # Second line input fields
                                        html.Div(
                                            children=[
                                                # Birthday
                                                html.Div(
                                                    children=[
                                                        "Birthday",
                                                        html.Br(),  # Line break
                                                        dcc.DatePickerSingle(
                                                            id="date-picker-bday",
                                                            placeholder="mm/dd/yyyy",  # Placeholder format
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
                                                # Patient age
                                                html.Div(
                                                    children=[
                                                        "Age",
                                                        html.Br(),  # Line break
                                                        dcc.Input(
                                                            id="age-input",  # ID for the input field
                                                            type="number",  # Type of the input field (text)
                                                            placeholder="20",  # Placeholder text for the input
                                                            style={"width": "50px", "padding": "5px", "margin-right": "20px", "font-style": "italic"}  # Input style
                                                        ),
                                                    ],
                                                    style={"text-align": "left"},  # Alignment
                                                ),

                                                  # Patient sex/gender
                                                    html.Div(
                                                        children=[
                                                            "Sex",
                                                            html.Br(),  # Line break
                                                            dcc.Dropdown(
                                                                id="gender-dropdown",  # ID for the dropdown
                                                                options=[
                                                                    {"label": "Female", "value": "Female"},
                                                                    {"label": "Male", "value": "Male"},
                                                                    {"label": "Others", "value": "Others"}
                                                                ],
                                                                placeholder="Select Gender",  # Placeholder text
                                                                style={
                                                                    "width": "250px", 
                                                                    "padding": "2px", 
                                                                    "margin-right": "20px", 
                                                                    "font-style": "italic"
                                                                }  # Dropdown style
                                                            ),

                                                        ],
                                                        style={"text-align": "left"},  # Alignment
                                                    ),

                                                    # Patient contact number
                                                    html.Div(
                                                        children=[
                                                            "Contact Number",
                                                            html.Br(),  # Line break
                                                            dcc.Input(
                                                                id="contact-input",  # ID for the input field
                                                                type="number",  # Type of the input field (text)
                                                                placeholder="0927 123 4567",  # Placeholder text for the input
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
                                                # Patient Civil Status
                                                html.Div(
                                                    children=[
                                                        "Civil Status",
                                                        html.Br(),  # Line break
                                                        dcc.Input(
                                                            id="civil-status-input",  # ID for the input field
                                                            type="text",  # Type of the input field (text)
                                                            placeholder="Single",  # Placeholder text for the input
                                                            style={"width": "250px", "padding": "5px", "margin-bottom": "50px", "font-style": "italic"}  # Input style
                                                        ),
                                                    ],
                                                    style={"margin-right": "20px", "text-align": "left"},  # Spacing and alignment
                                                ),
                                                # Patient Occupation
                                                html.Div(
                                                    children=[
                                                        "Occupation",
                                                        html.Br(),  # Line break
                                                        dcc.Input(
                                                            id="occupation-input",  # ID for the input field
                                                            type="text",  # Type of the input field (text)
                                                            placeholder="student",  # Placeholder text for the input
                                                            style={"width": "250px", "padding": "5px", "margin-right": "20px", "font-style": "italic"}  # Input style
                                                        ),
                                                    ],
                                                    style={"text-align": "left"},  # Alignment
                                                ),

                                                    # Patient address
                                                    html.Div(
                                                        children=[
                                                            "Address",
                                                            html.Br(),  # Line break
                                                            dcc.Input(
                                                                id="address-input",  # ID for the input field
                                                                type="text",  # Type of the input field (text)
                                                                placeholder="123 Roxas Ave, Diliman, Quezon City",  # Placeholder text for the input
                                                                style={"width": "345px", "padding": "5px", "font-style": "italic"}  # Input style
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
                                                    href="/patient_information",  # Link to the desired page (e.g., "/home")
                                                    style={"textDecoration": "none"}  # Remove underline from the link
                                                ),
                                                html.Button(
                                                    "Add",
                                                    id="add-button",
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
        html.Div(id="submit-status", style={"margin-top": "20px"}),
    ],
)

def register_callbacks(app):
    # Callback to add patient information to the database
    @app.callback(
        Output("submit-status", "children"),
        Input("add-button", "n_clicks"),
        [
            State("last-name-input", "value"),
            State("first-name-input", "value"),
            State("middle-name-input", "value"),
            State("address-input", "value"),
            State("contact-input", "value"),
            State("date-picker-bday", "date"),
            State("civil-status-input", "value"),
            State("occupation-input", "value"),
            State("gender-dropdown", "value"),
            State("age-input", "value"),
        ],
    )
    def add_patient(n_clicks, patient_last_name, patient_first_name, patient_middle_name, patient_address, patient_contact_number, patient_birthday, patient_civil_status, patient_occupation, patient_sex, patient_age):
        if not n_clicks or n_clicks == 0:
            raise PreventUpdate

        if not all([patient_last_name, patient_first_name, patient_middle_name, patient_address, patient_contact_number, patient_birthday, patient_civil_status, patient_occupation, patient_sex, patient_age]):
            return "Please fill in all fields."

        query = """
            INSERT INTO patient (patient_last_name, patient_first_name, patient_middle_name, patient_address, patient_contact_number, patient_birthday, patient_civil_status, patient_occupation, patient_sex, patient_age)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        data = (patient_last_name, patient_first_name, patient_middle_name, patient_address, patient_contact_number, patient_birthday, patient_civil_status, patient_occupation, patient_sex, patient_age)

        connection = create_connection()
        if not connection:
            return "Database connection failed."

        try:
            cursor = connection.cursor()
            cursor.execute(query, data)
            connection.commit()
            # Return the success message with fading effect
            return html.Div(
                "Patient information added successfully!",
                id="success-message",
                style={
                    "backgroundColor": "#28a745",  # Green background
                    "color": "white",              # White text
                    "padding": "10px",             # Padding for spacing
                    "borderRadius": "5px",         # Rounded corners
                    "textAlign": "center",         # Centered text
                    "transition": "opacity 2s ease-out",  # Smooth transition effect
                    "opacity": 1,                  # Full opacity initially
                }
            )
        except Exception as e:
            return f"An error occurred: {e}"
        finally:
            close_connection(connection)
            
    def patients_page_layout():
        return html.Div([
            dcc.Location(id="url", refresh=False),
            html.Div(id="submit-status"),  # Placeholder for error/success messages
            html.Div(id="success-message"),  # Success message will go here
            html.Div(id="patient-list"),
        ])