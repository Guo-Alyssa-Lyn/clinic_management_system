import dash_bootstrap_components as dbc
from dash import dcc, html, Output, Input, State
from dash.exceptions import PreventUpdate
from apps.dbconnect import create_connection, close_connection
from urllib.parse import parse_qs
import time

# Function to fetch service details from the database
def fetch_service_details(service_id):
    connection = create_connection()
    data = None
    if connection: 
        cursor = connection.cursor()
        query = """
        SELECT service_type, service_price
        FROM service
        WHERE service_id = %s
        """
        print(f"Executing query for service_id: {service_id}")  # Debugging line
        cursor.execute(query, (service_id,))
        data = cursor.fetchone()
        print(f"Query result: {data}")  # Debugging line
        close_connection(connection)
    else:
        print("Database connection failed.")  # Debugging line
    return data


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
        "marginTop":"0px",
        "marginBottom":"-30px",
    }
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
                            href="/medical_services",  # Link target (update to your desired path)
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
  

# The table - Edit Medical Services
html.Div(
    style={"padding": "0px"},
    children=[

        html.Div(
            style={"padding": "10px"},
            children=[ 
                html.Table(
                    style={
                        "width": "85%",
                        "margin-left": "90px",
                        "border": "1px solid black",
                        "border-collapse": "collapse",
                    },
                    children=[
                        html.Tr(
                            children=[
                                html.Th(
                                    children=["Edit Medical Service"],
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
                        html.Tr(
                            style={"border": "1px solid black"},
                            children=[
                                html.Td(
                                    children=[
                                        "Service Type",
                                        html.Br(),
                                        dcc.Input(
                                            id="service-type-input",
                                            type="text",
                                            placeholder="Enter service type",
                                            style={
                                                "width": "350px",
                                                "padding": "5px",
                                                "margin-top": "5px",
                                                "margin-bottom": "15px",
                                                "font-style": "italic",
                                            },
                                            value="",  # Initially empty until data is set
                                        ),
                                        html.Br(),
                                        "Service Fee (in Php)",
                                        html.Br(),
                                        dcc.Input(
                                            id="service-fee-input",
                                            type="number",
                                            placeholder="123.00",
                                            style={
                                                "width": "350px",
                                                "padding": "5px",
                                                "margin-top": "5px",
                                                "font-style": "italic",
                                            },
                                            value="",  # Initially empty until data is set
                                        ),
                                        html.Br(),
                                        # Cancel and Save Buttons
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
                                                    "Save",
                                                    id="save-button",
                                                    n_clicks=0,
                                                    style={
                                                        "background-color": "#4CAF50",
                                                        "font-size": "14px",
                                                        "color": "white",
                                                        "border-radius": "5px",
                                                        "padding": "5px 30px",
                                                        "margin-top": "40px",
                                                        "border": "none",
                                                        "cursor": "pointer",
                                                    },
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
                                        "padding-top": "20px",
                                        "padding-left": "40px",
                                        "padding-bottom": "20px",
                                        "padding-right": "20px",
                                        "text-align": "left",
                                        "background-color": "#f9f9f9",
                                        "font-weight": "bold",
                                        "color": "#05066d",
                                        "margin": "15px",
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
                html.Div(id='save-status'),
    ]
)

def edit_mode(app):
    # Callback to fetch and store service data in the store component
    @app.callback(
        Output('service-data-store', 'data'),
        Input("url", "search")  # Listening to changes in URL (assuming service_id is part of the query)
    )
    def fetch_and_store_data(search):
        start_time = time.time()  # Start timing the execution

        service_data = None
        if search:
            query_params = parse_qs(search[1:])  # Remove leading '?' and parse the query string
            service_id = query_params.get('service_id', [None])[0]  # Get the service_id
            if service_id:
                service_data = fetch_service_details(service_id)

        end_time = time.time()  # End timing the execution
        print(f"Callback execution time: {end_time - start_time} seconds")  # Debugging line

        if service_data:
            return {'service_type': service_data[0], 'service_fee': service_data[1]}
        else:
            return {'service_type': '', 'service_fee': ''}  # Default empty if no data

    # Callback to update input fields with data from store component
    @app.callback(
        [Output('service-type-input', 'value'),
         Output('service-fee-input', 'value')],
        Input('service-data-store', 'data')
    )
    def update_input_fields(service_data):
        if service_data:
            print(f"Updating input fields with service data: {service_data}")  # Debugging line
            return service_data.get('service_type', ''), service_data.get('service_fee', '')
        return '', ''  # Default to empty if no data is available

    # Callback to save the updated data back to the database
    @app.callback(
        Output('save-status', 'children'),  # Placeholder to display save status messages
        Input('save-button', 'n_clicks'),
        State('service-type-input', 'value'),
        State('service-fee-input', 'value'),
        State("url", "search")  # To retrieve the service_id from the URL
    )
    def save_service_data(n_clicks, service_type, service_fee, search):
        if n_clicks:  # Proceed only if the save button was clicked
            query_params = parse_qs(search[1:])  # Parse query parameters from the URL
            service_id = query_params.get('service_id', [None])[0]  # Get the service_id
            
            if not service_id:
                return "Error: Service ID is missing. Cannot save data."

            # Save updated data to the database
            connection = create_connection()
            if connection:
                try:
                    cursor = connection.cursor()
                    update_query = """
                        UPDATE service
                        SET service_type = %s, service_price = %s
                        WHERE service_id = %s
                    """
                    print(f"Updating service_id {service_id} with: {service_type}, {service_fee}")  # Debugging line
                    cursor.execute(update_query, (service_type, service_fee, service_id))
                    connection.commit()
                    print("Update successful.")  # Debugging line
                    return "Service details updated successfully."
                except Exception as e:
                    print(f"Database update error: {e}")  # Debugging line
                    return "An error occurred while updating the service details."
                finally:
                    close_connection(connection)  # Ensure the connection is closed
            else:
                print("Database connection failed.")  # Debugging line
                return "Failed to connect to the database."

        return "Click save to update the service details."