import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Output, Input, State
from dash.exceptions import PreventUpdate
from apps.dbconnect import create_connection, close_connection
from urllib.parse import parse_qs
import time

# Function to fetch service details from the database
def fetch_service_details(doctor_id):
    connection = create_connection()
    data = None
    if connection: 
        cursor = connection.cursor()
        query = """
        SELECT doctor_name, doctor_specialization, doctor_availability_date, doctor_availability_time
        FROM doctor
        WHERE doctor_id = %s
        """
        cursor.execute(query, (doctor_id,))
        data = cursor.fetchone()
        print(f"Query result: {data}")  # Debugging line

        # Check if data is fetched successfully
        if data and len(data) == 4:
            doctor_availability_time = data[3]  # Assuming the 4th column is doctor_availability_time
            
            # Split the availability time into start and end
            time_parts = doctor_availability_time.split(" - ")
            time_start_input = time_parts[0] if len(time_parts) > 0 else None
            time_end_input = time_parts[1] if len(time_parts) > 1 else None

            print(f"Time Start: {time_start_input}")  # Debugging line
            print(f"Time End: {time_end_input}")     # Debugging line

            # You can return or include this in the output
            result = {
                "doctor_name": data[0],
                "doctor_specialization": data[1],
                "doctor_availability_date": data[2],
                "time_start_input": time_start_input,
                "time_end_input": time_end_input
            }
            close_connection(connection)
            return result
    else:
        print("Database connection failed.")  # Debugging line
    return None

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

        # The table - Edit Doctor Schedule
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
                                        "Edit Doctor Schedule",
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
                                                # Doctor Name
                                                html.Div(
                                                    children=[
                                                        "Doctor Name",
                                                        html.Br(),  # Line break
                                                        dcc.Input(
                                                            id="doc-name-input-edit",  # ID for the input field
                                                            type="text",  # Type of the input field (text)
                                                            placeholder="Juan Dela Cruz",  # Placeholder text for the input
                                                            style={"width": "250px", "padding": "5px", "margin-bottom": "10px", "font-style": "italic"}  # Input style
                                                        ),
                                                    ],
                                                    style={"margin-right": "20px", "text-align": "left"},  # Spacing and alignment
                                                ),

                                                # Specialization
                                                html.Div(
                                                    children=[
                                                        "Specialization",
                                                        html.Br(),  # Line break
                                                        dcc.Input(
                                                            id="specialization-input-edit",  # ID for the input field
                                                            type="text",  # Type of the input field (text)
                                                            placeholder="Family Medicine",  # Placeholder text for the input
                                                            style={"width": "250px", "padding": "5px", "margin-right": "20px", "font-style": "italic"}  # Input style
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
                                                # Days Availability 
                                                html.Div(
                                                    children=[
                                                        "Days Availability",
                                                        html.Br(),
                                                        dcc.DatePickerSingle(
                                                            id="date-availability-edit",
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

                                                # Time Availability -start
                                                html.Div(
                                                    children=[
                                                        "Time Availability (Start)",
                                                        html.Br(),  # Line break
                                                        dcc.Input(
                                                            id="start-input-edit",  # ID for the input field
                                                            type="text",  # Type of the input field (text)
                                                            placeholder="00:00 AM",  # Placeholder text for the input
                                                            style={"width": "250px", "padding": "5px", "margin-right": "20px", "font-style": "italic"}  # Input style
                                                        ),
                                                    ],
                                                    style={"text-align": "left"},  # Alignment
                                                ), 

                                                # Time Availability -end
                                                html.Div(
                                                    children=[
                                                        "Time Availability (End)",
                                                        html.Br(),  # Line break
                                                        dcc.Input(
                                                            id="end-input-edit",  # ID for the input field
                                                            type="text",  # Type of the input field (text)
                                                            placeholder="00:00 AM",  # Placeholder text for the input
                                                            style={"width": "250px", "padding": "5px", "margin-right": "20px", "font-style": "italic"}  # Input style
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
                                                    href="/doctor_schedule",  # Replace with the target URL
                                                ),
                                                html.Button(
                                                    "Save",
                                                    id="save-button",
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
            html.Div(id='save-status-doctor-schedule'),
    ]
)

def edit_mode_doctor_sched(app):
    # Callback to fetch and store doctor data in the store component
    @app.callback(
        Output('doctor-data-store', 'data'),
        Input("url", "search")
    )
    def fetch_and_store_data(search):
        start_time = time.time()
        doctor_data = None

        if search:
            query_params = parse_qs(search[1:])
            doctor_id = query_params.get('doctor_id', [None])[0]
            if doctor_id:
                doctor_data = fetch_service_details(doctor_id)

        end_time = time.time()
        print(f"Callback execution time: {end_time - start_time} seconds")

        if doctor_data:
            return {
                'doctor_name': doctor_data["doctor_name"],
                'doctor_specialization': doctor_data["doctor_specialization"],
                'doctor_availability_date': doctor_data["doctor_availability_date"],
                'time_start_input': doctor_data["time_start_input"],
                'time_end_input': doctor_data["time_end_input"],
            }
        else:
            return {'doctor_name': '', 'doctor_specialization': '', 'doctor_availability_date': '', 'time_start_input': '', 'time_end_input': ''}

    # Callback to update input fields with data from the store component
    @app.callback(
        [
            Output('doc-name-input-edit', 'value'),
            Output('specialization-input-edit', 'value'),
            Output('date-availability-edit', 'date'),
            Output('start-input-edit', 'value'),
            Output('end-input-edit', 'value'),
        ],
        Input('doctor-data-store', 'data')
    )
    def update_input_fields(doctor_data):
        if doctor_data:
            return (
                doctor_data.get('doctor_name', ''),
                doctor_data.get('doctor_specialization', ''),
                doctor_data.get('doctor_availability_date', ''),
                doctor_data.get('time_start_input', ''),
                doctor_data.get('time_end_input', '')
            )
        return '', '', '', '', ''

    # Callback to save doctor data changes into the database
    @app.callback(
        Output('save-status-doctor-schedule', 'children'),  # Status message after save operation
        Input('save-button', 'n_clicks'),   # Triggered by save button click
        [
            State('doc-name-input-edit', 'value'),
            State('specialization-input-edit', 'value'),
            State('date-availability-edit', 'date'),
            State('start-input-edit', 'value'),
            State('end-input-edit', 'value'),
            State("url", "search")  # Capture doctor_id from URL
        ]
    )
    def save_doctor_data(n_clicks, name, specialization, availability_date, start_time, end_time, search):
        if n_clicks is None:
            return ""

        # Combine start and end times
        availability_time = f"{start_time} - {end_time}" if start_time and end_time else ""

        # Extract doctor_id from URL
        doctor_id = None
        if search:
            query_params = parse_qs(search[1:])
            doctor_id = query_params.get('doctor_id', [None])[0]

        if not doctor_id:
            return "Doctor ID not found. Cannot save data."

        # Update the database
        connection = create_connection()
        if connection:
            try:
                cursor = connection.cursor()
                query = """
                UPDATE doctor
                SET doctor_name = %s,
                    doctor_specialization = %s,
                    doctor_availability_date = %s,
                    doctor_availability_time = %s
                WHERE doctor_id = %s
                """
                cursor.execute(query, (name, specialization, availability_date, availability_time, doctor_id))
                connection.commit()
                return "Doctor data successfully saved!"
            except Exception as e:
                print(f"Error saving data: {e}")
                return "An error occurred while saving the data."
            finally:
                close_connection(connection)
        else:
            return "Database connection failed."