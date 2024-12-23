import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, State
from dash.exceptions import PreventUpdate
from apps.dbconnect import create_connection, close_connection

import pandas as pd

# Create a connection to the database
connection = create_connection()

# Fetch data from the database
data = []
if connection:
    cursor = connection.cursor()
    query = """
    SELECT service_id, service_type, service_price 
    FROM service
    """
    cursor.execute(query)
    data = cursor.fetchall()  # Fetch all rows from the query result
    close_connection(connection)  # Close the connection after fetching data

# Generate initial table rows
def generate_table_rows(data):
    return [
        html.Tr(
            key=f"row-{i}",
            children=[
                html.Td(
                    service[1],  # Display the service_type (service[1])
                    style={
                        "padding": "12px",
                        "text-align": "center",
                        "background-color": "#f9f9f9",
                        "color": "#05066d",
                        "border": "1px solid black",
                    },
                ),
                html.Td(
                    service[2],  # Display the service_price (service[2])
                    style={
                        "padding": "12px",
                        "text-align": "center",
                        "background-color": "#f9f9f9",
                        "color": "#05066d",
                        "border": "1px solid black",
                    },
                ),
                html.Td(
                    dcc.Link(
                        html.Button(
                            "Edit",
                            style={
                                "padding": "5px 20px",
                                "background-color": "#b0c5ff",
                                "font-size": "14px",
                                "font-weight": "bold",
                                "color": "#05066d",
                                "border": "none",
                                "cursor": "pointer",
                                "border-radius": "5px",
                            },
                        ),
                        href=f"/edit_medical_services_page?service_id={service[0]}",  # Pass the service_id via the URL
                    ),
                    style={
                        "padding": "12px",
                        "text-align": "center",
                        "background-color": "#f9f9f9",
                        "border": "1px solid black",
                    },
                ),
            ]
        )
        for i, service in enumerate(data)
    ]

# Define styles for the layout
styles = {
    "subHeader1": {
        "padding": "40px",
        "marginLeft": "60px"
    },
    "backHome": {
        "fontSize": "18px",
        "color": "#05066d",
        "marginTop": "-27px",
    },
    "medicalServices1": {
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

       # Section 1
        html.Div(
        style=styles["subHeader1"],
        children=[
        # Back to Home Page with an image icon on the left
        html.Div(
            children=[
                html.A(
                    href="/home",  # Link to the home page
                    children=[
                        html.Img(
                            src="/assets/resources/Arrow Icon.png",  # Path to the icon image
                            style={
                                "margin-right": "8px",  # Space between icon and text
                                "width": "16px",  # Adjust icon size
                                "height": "16px",  # Keep consistent size
                            },
                        ),
                        "Back to Home Page",  # Text
                    ],
                    style={
                        "text-decoration": "none",  # Remove underline
                        "color": "#05066d",  # Link text color
                        "font-weight": "bold",  # Bold text
                        "display": "inline-flex",  # Align image and text inline
                        "align-items": "center",  # Vertically center align
                    },
                ),
            ],
            style={"margin-bottom": "50px"},  # Add 50px margin below this section
        ),
        html.P("Medical Services", style=styles["medicalServices1"]),
        html.Hr(style=styles["divider1"]),
        # Button wrapped inside dcc.Link to navigate to another page
        dcc.Link(
            html.Button(
                'Add New Medical Service',
                id='add-service-button',
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
            href='/add_medical_services',  # The target URL for the link
            style={'text-decoration': 'none'}  # Optional styling to remove link underline
        ),
    ],
),

    # The table box
    html.Div(
            style={"padding": "0px"},
            children=[
                html.Div(
                    style={"padding": "10px"},
                    children=[
                        html.Table(
                            style={
                                "width": "35%",
                                "margin-left": "90px",
                                "border": "1px solid black",
                                "margin-top": "-30px",
                                "border-collapse": "collapse",
                            },
                            children=[
                                html.Tr(
                                    children=[
                                        html.Th(
                                            "Search Medical Services",
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
                                                "Service Type",
                                                html.Br(),
                                                dcc.Input(
                                                    id="search-bar",
                                                    type="text",
                                                    placeholder="Enter service type",
                                                    style={
                                                        "width": "100%",
                                                        "padding": "5px",
                                                        "margin-top": "5px",
                                                        "font-style": "italic",
                                                    },
                                                ),
                                            ],
                                            style={
                                                "padding": "25px",
                                                "text-align": "left",
                                                "background-color": "#f9f9f9",
                                                "font-weight": "bold",
                                                "color": "#05066d",
                                            },
                                        ),
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
                html.H3("Medical Services", style=styles["medicalServices2"]),
            ],
        ),

            # Table list for medical services
            html.Div(
    id="service-table",
    style={"padding": "0px"},
    children=[
        html.Div(
            style={"padding": "10px"},
            children=[
                html.Table(
                    style={
                        "width": "85%",
                        "margin-left": "88px",
                        "margin-right": "auto",
                        "margin-top": "-30px",
                        "border": "1px solid black",
                        "border-collapse": "collapse",
                    },
                    children=[
                        html.Thead(
                            children=[
                                html.Tr(
                                    children=[
                                        html.Th(
                                            "Service Type",
                                            style={
                                                "padding": "12px",
                                                "text-align": "center",
                                                "font-weight": "bold",
                                                "background-color": "#05066d",
                                                "color": "white",
                                                "border": "1px solid black",
                                                "width": "33%",
                                            },
                                        ),
                                        html.Th(
                                            "Service Fee (in Php)",
                                            style={
                                                "padding": "12px",
                                                "text-align": "center",
                                                "font-weight": "bold",
                                                "background-color": "#05066d",
                                                "color": "white",
                                                "border": "1px solid black",
                                                "width": "33%",
                                            },
                                        ),
                                        html.Th(
                                            "Action",
                                            style={
                                                "padding": "12px",
                                                "text-align": "center",
                                                "font-weight": "bold",
                                                "background-color": "#05066d",
                                                "color": "white",
                                                "border": "1px solid black",
                                                "width": "34%",
                                            },
                                        ),
                                    ]
                                )
                            ]
                        ),
                        html.Tbody(
                            id="service-table-body",  # Dynamic table body for callback updates
                            children=generate_table_rows(data),  # Initial rows
                        ),
                    ], 
                )
            ],
        )
    ],
),
    ]
)

# Callback to filter the table based on search input
def filter_search(app): 
    @app.callback(
        Output("service-table-body", "children"),
        Input("search-bar", "value"),
    )
    def filter_table(search_query):
        if not search_query:  # If no search query, return all rows
            return generate_table_rows(data)

        # Filter rows based on the search query
        filtered_data = [
            service for service in data
            if search_query.lower() in str(service[0]).lower() or search_query.lower() in str(service[1]).lower()
        ]
        return generate_table_rows(filtered_data)