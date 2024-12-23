import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, State
from dash.exceptions import PreventUpdate
from apps.dbconnect import create_connection, close_connection
import dash 

# Define styles for the layout
styles = {
    "subHeader1": {
        "padding": "40px",
        "marginLeft": "60px"
    },
    "backAppointmentSched": {
        "fontSize": "18px",
        "color": "#05066d",
    },
    "appointSched": {
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

        html.Div(
            id="page-load-trigger",
            style={"display": "none"},
            children="initial"  # Add an initial value
        ),
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
                                "Back to Appointment Schedule Page"
                            ],
                            href="/book_appointment",  # Link target
                            style={
                                **styles["backAppointmentSched"],  # Apply existing styles
                                "text-decoration": "none",  # Remove underline
                                "color": "inherit",  # Ensure link text inherits color from parent
                            },
                        ),
                    ],
                    style={"margin-bottom": "50px"},  # Add margin between this and the next section
                ),
                html.P("Appointments Schedule", style=styles["appointSched"]),
                html.Hr(style=styles["divider1"]),
            ],
        ),


        # The table - Add New Appointment Schedule
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
                        "margin-top": "-50px",
                        "border": "1px solid black",
                        "border-collapse": "collapse",
                    },
                    children=[
                        html.Tr(
                            children=[
                                html.Th(
                                    children=["Add New Appointment Schedule"],
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
                                        # Wrapper for flex layout
                                        html.Div(
                                            children=[
                                                html.Div(
                                                    children=[
                                                        "Patient Name",
                                                        html.Br(),
                                                        dcc.Input(
                                                            id="full-name-input",
                                                            type="text",
                                                            placeholder="Juan Dela Cruz",
                                                            style={
                                                                "width": "250px",
                                                                "padding": "5px",
                                                                "margin-bottom": "10px",
                                                                "margin-right": "10px",
                                                                "font-style": "italic",
                                                            },
                                                        ),
                                                    ],
                                                    style={"margin-right": "20px", "text-align": "left"},
                                                ),
                                                html.Div(
                                                    className="medical-service-container",  # Add the class name here
                                                    children=[
                                                        "Medical Service",
                                                        html.Br(),
                                                        dcc.Dropdown(
                                                            id="medical-service-dropdown-add",
                                                            options=[],
                                                            placeholder="Select a service type",
                                                            value=None,
                                                            clearable=True,
                                                            style={
                                                                "width": "300px",
                                                                "padding": "0px",
                                                                "margin-bottom": "10px",
                                                                "margin-right": "20px",
                                                                "font-style": "italic",
                                                            },
                                                        ),
                                                    ],
                                                    style={"margin-right": "20px", "text-align": "left"},
                                                ),
                                            ],
                                            style={"display": "flex", "gap": "20px"},
                                        ),
                                        html.Div(
                                            children=[
                                                # Appointment Date and Time (Start & End) Inline (Flex)
                                                html.Div(
                                                    children=[
                                                        html.Div(
                                                            children=[
                                                                "Appointment Date",
                                                                html.Br(),
                                                                dcc.DatePickerSingle(
                                                                    id="date-picker-appointment",
                                                                    placeholder="MM/DD/YYYY",
                                                                    display_format="MM/DD/YYYY",
                                                                    style={
                                                                        "margin-right": "20px",
                                                                        "margin-bottom": "10px",
                                                                        "width": "150px",
                                                                    },
                                                                    className="custom-date-picker",
                                                                ),
                                                            ],
                                                            style={"margin-right": "20px", "text-align": "left"},
                                                        ),
                                                        # Appointment Time
                                                        html.Div(
                                                            children=[
                                                                "Appointment Time (Start)",
                                                                html.Br(),
                                                                html.Div(
                                                                    children=[
                                                                        dcc.Dropdown(
                                                                            id='start-hour-dropdown',
                                                                            options=[{'label': f'{i%12 if i%12 != 0 else 12}', 'value': i} for i in range(1, 13)],
                                                                            value=8,
                                                                            style={"width": "90px"}
                                                                        ),
                                                                        dcc.Dropdown(
                                                                            id='start-minute-dropdown',
                                                                            options=[{'label': f'{i:02d}', 'value': f'{i:02d}'} for i in range(0, 60, 5)],
                                                                            value='00',
                                                                            style={"width": "80px"}
                                                                        ),
                                                                        dcc.Dropdown(
                                                                            id='start-ampm-dropdown',
                                                                            options=[{'label': 'AM', 'value': 'AM'}, {'label': 'PM', 'value': 'PM'}],
                                                                            value='AM',
                                                                            style={"width": "80px"}
                                                                        ),
                                                                    ],
                                                                    style={"display": "flex", "gap": "10px", "text-align": "left"},
                                                                ),
                                                            ],
                                                            style={"flex-direction": "column", "display": "flex", "gap": "5px", "text-align": "left", "margin-left": "80px", "margin-bottom": "15px"},
                                                        ),
                                                    ],
                                                    style={"display": "flex", "gap": "30px", "align-items": "center"},
                                                ),
                                            ],
                                            style={"display": "flex", "gap": "20px"},
                                        ),
                                        html.Div(
                                            children=[
                                                html.Div(
                                                    children=[
                                                        "Contact Number",
                                                        html.Br(),
                                                        dcc.Input(
                                                            id="contact-input",
                                                            type="text",
                                                            placeholder="09xx xxx xxx",
                                                            style={
                                                                "width": "250px",
                                                                "padding": "5px",
                                                                "margin-right": "10px",
                                                                "font-style": "italic",
                                                            },
                                                        ),
                                                    ],
                                                    style={"margin-right": "20px", "text-align": "left"},
                                                ),
                                                html.Div(
                                                    children=[
                                                        "Secretary Name",
                                                        html.Br(),
                                                        dcc.Dropdown(
                                                            id="secretary-name-dropdown-add",
                                                            options=[],
                                                            placeholder="Select a staff",
                                                            style={
                                                                "width": "300px",
                                                                "padding": "0px",
                                                                "margin-bottom": "10px",
                                                                "margin-right": "20px",
                                                                "font-style": "italic",
                                                            },
                                                        ),
                                                    ],
                                                    style={"margin-right": "20px", "text-align": "left"},
                                                ),
                                            ],
                                            style={"display": "flex", "gap": "20px"},
                                        ),
                                        # Buttons
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
                                                        href="/book_appointment",  # Replace with the target URL
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
                                                        "cursor": "pointer",
                                                    },
                                                ),
                                            ],
                                            style={"margin-top": "10px", "text-align": "right", "width": "100%"},
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
        html.Div(id="submit-show", style={"margin-top": "20px"}),
    ]
)

def register_callbacks(app):
    @app.callback(
        [
            Output("medical-service-dropdown-add", "options"),
            Output("secretary-name-dropdown-add", "options")
        ],
        Input("page-load-trigger", "children"),
        prevent_initial_call=False
    )
    def update_dropdown_options(trigger):
        print(f"\n=== Starting Dropdowns Data Fetch === Trigger value: {trigger}")
        connection = create_connection()
        if not connection:
            print("Database connection failed.")
            return [], []

        try:
            cursor = connection.cursor(dictionary=True)
            
            # Fetch service types with IDs
            service_query = "SELECT service_id, service_type FROM service"
            print(f"Executing service query: {service_query}")
            cursor.execute(service_query)
            service_results = cursor.fetchall()
            print(f"Raw service results: {service_results}")
            
            # Process service options with IDs as values
            service_options = []
            for row in service_results:
                if row['service_type'] and row['service_id']:
                    option = {"label": row['service_type'], "value": row['service_id']}
                    service_options.append(option)
                    print(f"Added service option: {option}")
            
            # Fetch secretary names with IDs
            secretary_query = "SELECT secretary_id, secretary_name FROM clinic_secretary"
            print(f"Executing secretary query: {secretary_query}")
            cursor.execute(secretary_query)
            secretary_results = cursor.fetchall()
            print(f"Raw secretary results: {secretary_results}")
            
            # Process secretary options with IDs as values
            secretary_options = []
            for row in secretary_results:
                if row['secretary_name'] and row['secretary_id']:
                    option = {"label": row['secretary_name'], "value": row['secretary_id']}
                    secretary_options.append(option)
                    print(f"Added secretary option: {option}")
            
            print(f"Final service options: {service_options}")
            print(f"Final secretary options: {secretary_options}")
            
            return service_options, secretary_options

        except Exception as e:
            print(f"Error in dropdown data fetch: {str(e)}")
            import traceback
            print(f"Traceback: {traceback.format_exc()}")
            return [], []
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
            print("=== End Dropdowns Data Fetch ===\n")

    @app.callback(
        Output("page-load-trigger", "children"),
        Input("medical-service-dropdown-add", "id"),
        prevent_initial_call=False
    )
    def initialize_dropdown(dropdown_id):
        print(f"Initializing dropdown trigger for {dropdown_id}")
        return "loaded"
    
    @app.callback(
        Output("contact-input", "value"),
        Input("full-name-input", "value")
    )
    def fetch_contact_number(patient_full_name):
        if not patient_full_name:
            raise PreventUpdate

        connection = create_connection()
        if not connection:
            return dash.no_update

        try:
            cursor = connection.cursor()
            query = """
                SELECT patient_contact_number
                FROM patient
                WHERE CONCAT(patient_first_name, ' ', COALESCE(patient_middle_name, ''), ' ', patient_last_name) = %s
            """
            cursor.execute(query, (patient_full_name,))
            result = cursor.fetchone()

            return result[0] if result else ""
        except Exception as e:
            print(f"Error fetching contact number: {e}")
            return dash.no_update
        finally:
            close_connection(connection)

    @app.callback(
        Output("submit-show", "children"),
        Input("add-button", "n_clicks"),
        [
            State("full-name-input", "value"),
            State("medical-service-dropdown-add", "value"),
            State("contact-input", "value"),
            State("secretary-name-dropdown-add", "value"),
            State("date-picker-appointment", "date"),
            State("start-hour-dropdown", "value"),
            State("start-minute-dropdown", "value"),
            State("start-ampm-dropdown", "value"),
        ],
    )
    def handle_form_submission(n_clicks, patient_full_name, service_id, contact_number, 
                             secretary_id, appointment_date, start_hour, start_minute, start_ampm):
        if not n_clicks:
            raise PreventUpdate

        if not all([patient_full_name, service_id, secretary_id, 
                   appointment_date, start_hour, start_minute, start_ampm]):
            return "Please fill in all fields."

        connection = create_connection()
        if not connection:
            return "Database connection failed."

        try:
            cursor = connection.cursor()

            # Fetch patient ID
            fetch_query = """
                SELECT patient_id
                FROM patient
                WHERE CONCAT(patient_first_name, ' ', COALESCE(patient_middle_name, ''), ' ', patient_last_name) = %s
            """
            cursor.execute(fetch_query, (patient_full_name,))
            result = cursor.fetchone()

            if not result:
                return f"The patient {patient_full_name} does not exist yet."

            patient_id = result[0]

            # Insert appointment details with service_id and secretary_id
            appointment_time = f"{start_hour}:{start_minute} {start_ampm}"
            insert_query = """
                INSERT INTO appointment (
                    patient_id, 
                    service_id,
                    secretary_id,
                    appointment_date, 
                    appointment_time
                )
                VALUES (%s, %s, %s, %s, %s)
            """
            data = (patient_id, service_id, secretary_id, appointment_date, appointment_time)
            cursor.execute(insert_query, data)
            connection.commit()

            return html.Div(
                f"New appointment added successfully for {patient_full_name}!",
                id="success-message",
                style={
                    "backgroundColor": "#28a745",
                    "color": "white",
                    "padding": "10px",
                    "borderRadius": "5px",
                    "textAlign": "center",
                    "transition": "opacity 2s ease-out",
                    "opacity": 1,
                },
            )
        except Exception as e:
            return f"An error occurred: {e}"
        finally:
            close_connection(connection)