import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, State
from dash.exceptions import PreventUpdate
import bcrypt  # Import bcrypt for password hashing
from apps.dbconnect import create_connection, close_connection

# Define styles for the layout
styles = {
    "subHeader1": {
        "padding": "40px", 
        "marginLeft": "60px"
    },
    "backClinicTeam": {
        "fontSize": "18px",
        "color": "#05066d",
    },
    "clinicTeam": {
        "fontWeight": "bold",
        "fontSize": "30px",
        "color": "#05066d",
    },
    "divider1": {
        "width": "93%",
        "border": "2px solid #05066d",
        "marginTop": "-15px",
        "marginLeft": "-0px"
    },
}

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
                                "Back to Clinic Team Page"
                            ],
                            href="/clinic_employee",  # Link target
                            style={
                                **styles["backClinicTeam"],  # Apply existing styles
                                "text-decoration": "none",  # Remove underline
                                "color": "inherit",  # Ensure link text inherits color from parent
                            },
                        ),
                    ],
                    style={"margin-bottom": "50px"},  # Add margin between this and the next section
                ),
                html.P("Clinic Team", style=styles["clinicTeam"]),
                html.Hr(style=styles["divider1"]),
            ],
        ),

            # The table - Add New Clinic Employee
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
                                        "Add New Employee",
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
                                                # Employee Full Name
                                                html.Div( 
                                                    children=[
                                                        "Employee Name",
                                                        html.Br(),  # Line break
                                                        dcc.Input(
                                                            id="employee-name-input",  # ID for the input field
                                                            type="text",  # Type of the input field (text)
                                                            placeholder="Juan Dela Cruz",  # Placeholder text for the input
                                                            style={"width": "250px", "padding": "5px", "margin-bottom": "10px", "margin-right": "30px", "font-style": "italic"}  # Input style
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
                                                # Email
                                                html.Div(
                                                    children=[
                                                        "Email",
                                                        html.Br(),  # Line break
                                                        dcc.Input(
                                                            id="email-input",  # ID for the input field
                                                            type="text",  # Type of the input field (text)
                                                            placeholder="Enter email",  # Placeholder text for the input
                                                            style={"width": "250px", "padding": "5px", "margin-right": "30px", "font-style": "italic"}  # Input style
                                                        ),
                                                    ],
                                                    style={"margin-right": "20px", "text-align": "left"},  # Spacing and alignment
                                                ),
                                                # Password
                                                html.Div(
                                                    children=[
                                                        "Password",
                                                        html.Br(),  # Line break
                                                        dcc.Input(
                                                            id="password-input",  # ID for the input field
                                                            type="text",  # Type of the input field (text)
                                                            placeholder="Enter password",  # Placeholder text for the input
                                                            style={"width": "250px", "padding": "5px", "margin-right": "30px", "font-style": "italic"}  # Input style
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
                                                # Role
                                                html.Div(
                                                    children=[
                                                        "Role",
                                                        html.Br(),  # Line break
                                                        dcc.Input(
                                                            id="role-input",  # ID for the input field
                                                            type="text",  # Type of the input field (text)
                                                            placeholder="Enter Role",  # Placeholder text for the input
                                                            style={"width": "250px", "padding": "5px", "margin-right": "30px", "font-style": "italic"}  # Input style
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
                                                        href="/clinic_employee",  # Replace with the target URL
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
    html.Div(id="submit-done", style={"margin-top": "20px"}),
])

def register_callbacks(app):
    # Callback to add patient information to the database
    @app.callback(
        Output("submit-done", "children"),
        Input("add-button", "n_clicks"),
        [
            State("employee-name-input", "value"),
            State("email-input", "value"),
            State("password-input", "value"),
            State("role-input", "value")
        ],
    )
    def add_patient(n_clicks, secretary_name, secretary_email, secretary_password, secretary_role):
        if not n_clicks or n_clicks == 0:
            raise PreventUpdate

        if not all([secretary_name, secretary_email, secretary_password, secretary_role]):
            return "Please fill in all fields."

        # Hash the password
        hashed_password = bcrypt.hashpw(secretary_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        query = """
            INSERT INTO clinic_secretary (secretary_name, secretary_email, secretary_password, secretary_role)
            VALUES (%s, %s, %s, %s)
        """
        data = (secretary_name, secretary_email, hashed_password, secretary_role)

        connection = create_connection()
        if not connection:
            return "Database connection failed."

        try:
            cursor = connection.cursor()
            cursor.execute(query, data)
            connection.commit()
            # Return the success message with fading effect
            return html.Div(
                "New employee added successfully!",
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
            html.Div(id="submit-done"),  # Placeholder for error/success messages
            html.Div(id="success-message"),  # Success message will go here
            html.Div(id="patient-list"),
        ])
