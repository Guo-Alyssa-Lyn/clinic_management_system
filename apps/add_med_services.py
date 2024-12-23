import dash
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
    "backMedicalServices": {
        "fontSize": "18px",
        "marginBottom": "50px",
        "marginTop": "-30px",
        "color": "#05066d",
    },
    "medicalServicesSubHeader": {
        "fontWeight": "bold",
        "fontSize": "30px",
        "color": "#05066d",
    },
    "divider": {
        "width": "93%", 
        "border": "2px solid #05066d",
        "marginBottom":"-30px",
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
                                "Back to Medical Services Page"
                            ],
                            href="/medical_services",  # Link to the Medical Services page
                            style={
                                **styles["backMedicalServices"],  # Apply existing styles
                                "text-decoration": "none",  # Remove underline
                                "color": "inherit"  # Ensure link text inherits color from parent
                            },
                        ),
                    ],
                    style={"margin-bottom": "50px"},
                ),
                html.H2("Medical Services", style=styles["medicalServicesSubHeader"]),
                html.Hr(style=styles["divider"]),
            ],
        ),


# The table - Add Medical Services
html.Div(
    style={"padding": "0px"},
    children=[
        html.Div(
            style={"padding": "10px"},
            children=[
                # Table Container with smaller width
                html.Table(
                    style={
                        "width": "85%",  # table width
                        "margin-left": "90px",  # Move the table to the left
                        
                        "border": "1px solid black", 
                        "border-collapse": "collapse", 
                    },
                    children=[
                        # Table Header Row
                        html.Tr(
                            children=[
                                html.Th(
                                    children=[
                                        "Add Medical Service",
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
                                        # Service Type Input
                                        "Service Type",
                                        html.Br(),  # Line break
                                        dcc.Input(
                                            id="service-type-input",  # ID for the input field
                                            type="text",  # Type of the input field (text)
                                            placeholder="Enter service type",  # Placeholder text for the input
                                            style={"width": "350px", "padding": "5px", "margin-top": "5px", "margin-bottom": "15px", "font-style": "italic"}  # Reduced size
                                        ),
                                        html.Br(),  # Line break between inputs

                                        # Service Fee Input
                                        "Service Fee (in Php)",
                                        html.Br(),  # Line break
                                        dcc.Input(
                                            id="service-fee-input",  # ID for the input field
                                            type="number",  # Type of the input field (number)
                                            placeholder="123.00",  # Placeholder text for the input
                                            style={"width": "350px", "padding": "5px", "margin-top": "5px", "font-style": "italic"}  # Reduced size
                                        ),
                                        html.Br(),  # Line break between inputs

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
                                                        href="/medical_services",  # Replace with the target URL
                                                    ),
                                                html.Button(
                                                    "Add",
                                                    id="add-button",
                                                    n_clicks=0,
                                                    style={
                                                        "background-color": "#4CAF50", 
                                                        "font-size": "13px",
                                                        "font-weight": "bold",
                                                        "color": "white", 
                                                        "border-radius": "5px",
                                                        "padding": "5px 35px", 
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
                                        "padding": "30px", 
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
        html.Div(id="submit-news", style={"margin-top": "20px"}),
    ]
)

def register_callbacks(app):
    # Callback to add patient information to the database
    @app.callback(
        Output("submit-news", "children"),
        Input("add-button", "n_clicks"),
        [
            State("service-type-input", "value"),
            State("service-fee-input", "value"),
        ],
    )
    def add_patient(n_clicks, service_type, service_fee):
        if not n_clicks or n_clicks == 0:
            raise PreventUpdate

        if not all([service_type, service_fee]):
            return "Please fill in all fields."

        query = """
            INSERT INTO service (service_type, service_price)
            VALUES (%s, %s)
        """
        data = (service_type, service_fee)

        connection = create_connection()
        if not connection:
            return "Database connection failed."

        try:
            cursor = connection.cursor()
            cursor.execute(query, data)
            connection.commit()
            # Return the success message with fading effect
            return html.Div(
                "Medical Services added successfully!",
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
            html.Div(id="submit-news"),  # Placeholder for error/success messages
            html.Div(id="success-message"),  # Success message will go here
            html.Div(id="patient-list"),
        ])