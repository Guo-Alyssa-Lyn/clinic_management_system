import dash_bootstrap_components as dbc
from dash import dcc, html, Output, Input, State
from dash.exceptions import PreventUpdate
from apps.dbconnect import create_connection, close_connection
from urllib.parse import parse_qs
import traceback
import time
from datetime import datetime, date

# Define styles for the layout
styles = {
    "subHeader1": {
        "padding": "40px",
        "marginLeft": "60px"
    },
    "backPaymentRecord": {
        "fontSize": "18px",
        "marginTop": "-30px",
        "color": "#05066d"
    },
    "paymentRecords": {
        "fontSize": "30px",
        "color": "#05066d",
        "fontWeight": "bold"
    },
    "divider1": {
        "width": "93%",
        "border": "2px solid #05066d",
        "marginTop": "-3px"
    },
}

# Set up routing and layout
layout = html.Div(
    children=[

dcc.Store(id='payment-edit-data-store', storage_type='memory'), 

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
                                "Back to Payment Records Page"
                            ],
                            href="/payment",  # Link target
                            style={
                                **styles["backPaymentRecord"],  # Apply existing styles
                                "text-decoration": "none",  # Remove underline
                                "color": "inherit"  # Ensure link text inherits color from parent
                            },
                        ),
                    ],
                    style={"margin-bottom": "50px"},
                ),
                html.H2("Payment Records", style=styles["paymentRecords"]),
                html.Hr(style=styles["divider1"]),
            ],
        ),  

        # The table - Add New Patient
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
                                        "Edit Payment Record",
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
                                                # Patient Full Name
                                                html.Div(
                                                    children=[
                                                        "Patient Name",
                                                        html.Br(),  # Line break
                                                        dcc.Input(
                                                            id="fullname-input-modify",  # ID for the input field
                                                            type="text",  # Type of the input field (text)
                                                            placeholder="Juan Dela Cruz",  # Placeholder text for the input
                                                            style={"width": "250px", "padding": "5px", "margin-right": "50px", "font-style": "italic"}  # Input style
                                                        ),
                                                    ],
                                                    style={"margin-right": "20px", "text-align": "left"},  # Spacing and alignment
                                                ),
                                                # Appointment Date
                                                dcc.DatePickerSingle(
                                                    id="date-picker-appointment-modify",
                                                    min_date_allowed=date(2000, 1, 1),
                                                    max_date_allowed=date(2030, 12, 31),
                                                    initial_visible_month=date.today(),
                                                    display_format='YYYY-MM-DD',  # Changed format to match database
                                                    placeholder='YYYY-MM-DD',
                                                    date=None,  # This will be updated by the callback
                                                    style={
                                                        "margin-right": "220px",
                                                        "margin-bottom": "15px",
                                                        "width": "100px",
                                                    },
                                                    className="custom-date-picker"
                                                ),

                                                # Doctor Full Name
                                                html.Div(
                                                    children=[
                                                        "Doctor Name",
                                                        html.Br(),  # Line break
                                                        dcc.Input(
                                                            id="doctor-name-input-modify",  # ID for the input field
                                                            type="text",  # Type of the input field (text)
                                                            placeholder="Tony Jarvis",  # Placeholder text for the input
                                                            style={"width": "250px", "padding": "5px", "font-style": "italic"}  # Input style
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
                                                # Payment method
                                                html.Div(
                                                    children=[
                                                        "Payment Method",
                                                        html.Br(),
                                                        dcc.RadioItems(
                                                            id="payment-method-modify",
                                                            options=[
                                                                {"label": "Cash", "value": "Cash"},
                                                                {"label": "Gcash", "value": "Gcash"},
                                                            ],
                                                            style={
                                                                "width": "250px",
                                                                "margin-right": "20px",
                                                            },
                                                            labelStyle={
                                                                "display": "inline-block",
                                                                "margin-right": "15px",
                                                            },
                                                        ),
                                                    ],
                                                    style={
                                                        "margin-right": "20px",
                                                        "text-align": "left",
                                                        "min-width": "300px",
                                                    },
                                                ),

                                                # Payment status
                                                html.Div(
                                                    children=[
                                                        "Payment Method",
                                                        html.Br(),
                                                        dcc.RadioItems(
                                                            id="payment-status-modify",
                                                            options=[
                                                                {"label": "Paid", "value": "Paid"},
                                                                {"label": "Unpaid", "value": "Unpaid"},
                                                            ],
                                                            style={
                                                                "width": "250px",
                                                                "margin-right": "20px",
                                                            },
                                                            labelStyle={
                                                                "display": "inline-block",
                                                                "margin-right": "10px",
                                                            },
                                                        ),
                                                    ],
                                                    style={
                                                        "margin-right": "20px",
                                                        "text-align": "left",
                                                        "min-width": "300px",
                                                    },
                                                ),

                                                  # Amount Input
                                                    html.Div(
                                                        children=[
                                                            "Amount Input (in Php)",
                                                            html.Br(),  # Line break
                                                            dcc.Input(
                                                            id="amount-input-modify",  # ID for the input field
                                                            type="number",  # Type of the input field (text)
                                                            placeholder="123.00",  # Placeholder text for the input
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

                                        # Buttons: Cancel and Add (Aligned to the right)
                                        html.Div(
                                            children=[
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
                                                        "margin-right": "30px", 
                                                        "margin-top": "40px", 
                                                        "border": "none", 
                                                        "cursor": "pointer"
                                                    }
                                                ),
                                                html.Button(
                                                    "Save",
                                                    id="save-edit-changes-button",
                                                    n_clicks=0,
                                                    style={
                                                        "background-color": "#4CAF50", 
                                                        "color": "white", 
                                                        "font-size": "14px",
                                                        "font-weight": "bold",
                                                        "padding": "5px 40px",
                                                        "border-radius": "5px",
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
    html.Div(id='save-status-edit-payment'),
    ]
)

def edit_mode_payment_details(app):
    @app.callback(
    Output('payment-edit-data-store', 'data'),
    Input("url", "pathname")
    )
    def fetch_and_store_data(pathname):
        print("\n=== Debug: fetch_and_store_data started ===")
        print(f"Pathname received: {pathname}")
        
        try:
            # Extract patient_id from pathname
            patient_id = pathname.split('/')[-1]  # Gets '5' from '/edit_payment_mode/5'
            print(f"Extracted patient_id: {patient_id}")
            
            if not patient_id:
                print("No patient ID found")
                return {}

            # Get the payment data
            payment_data = fetch_service_details(patient_id)
            print(f"Payment data fetched: {payment_data}")
            
            if payment_data:
                formatted_data = {
                    'payment_method': payment_data.get('payment_method', ''),
                    'payment_status': payment_data.get('payment_status', ''),
                    'payment_amount': payment_data.get('payment_amount', ''),
                    'full_name': f"{payment_data.get('patient_first_name', '')} {payment_data.get('patient_last_name', '')}".strip(),
                    'doctor_name': payment_data.get('doctor_name', ''),
                    'appointment_date': payment_data.get('appointment_date')
                }
                print(f"Formatted data: {formatted_data}")
                return formatted_data
                
            return {}

        except Exception as e:
            print(f"Error in fetch_and_store_data: {e}")
            print(traceback.format_exc())
            return {}

    @app.callback(
        [
            Output('fullname-input-modify', 'value'),
            Output('date-picker-appointment-modify', 'date'),
            Output('doctor-name-input-modify', 'value'),
            Output('payment-method-modify', 'value'),
            Output('payment-status-modify', 'value'),
            Output('amount-input-modify', 'value'),
        ],
        Input('payment-edit-data-store', 'data'),
    )
    def update_input_fields(payment_data):
        print("\n=== Debug: update_input_fields started ===")
        print(f"Received payment data: {payment_data}")

        if payment_data is None or not payment_data:
            print("No payment data received")
            return '', None, '', None, None, ''

        try:
            # Get the values with default fallbacks
            full_name = payment_data.get('full_name', '')
            appointment_date = payment_data.get('appointment_date')
            doctor_name = payment_data.get('doctor_name', '')
            payment_method = payment_data.get('payment_method', '')
            payment_status = payment_data.get('payment_status', '')
            payment_amount = payment_data.get('payment_amount', '')

            print(f"""
                Returning values:
                - full_name: {full_name}
                - appointment_date: {appointment_date}
                - doctor_name: {doctor_name}
                - payment_method: {payment_method}
                - payment_status: {payment_status}
                - payment_amount: {payment_amount}
            """)

            return full_name, appointment_date, doctor_name, payment_method, payment_status, payment_amount

        except Exception as e:
            print(f"Error in update_input_fields: {e}")
            print(traceback.format_exc())
            return '', None, '', None, None, ''

    def fetch_service_details(patient_id):
        print(f"\n=== Fetching data for patient_id: {patient_id} ===")
        
        connection = create_connection()
        if not connection:
            print("Database connection failed")
            return None

        try:
            cursor = connection.cursor(dictionary=True)
            
            # Modified query to ensure proper joins
            query = """
                SELECT 
                    p.payment_method, 
                    p.payment_status, 
                    p.payment_amount,
                    pat.patient_first_name, 
                    pat.patient_last_name,
                    d.doctor_name, 
                    DATE_FORMAT(a.appointment_date, '%Y-%m-%d') as appointment_date
                FROM patient pat
                LEFT JOIN appointment a ON pat.patient_id = a.patient_id
                LEFT JOIN payment p ON a.appointment_id = p.appointment_id
                LEFT JOIN doctor d ON a.doctor_id = d.doctor_id
                WHERE pat.patient_id = %s
                ORDER BY a.appointment_date DESC
                LIMIT 1
            """
            
            print(f"Executing query: {query}")
            print(f"With patient_id: {patient_id}")
            
            cursor.execute(query, (patient_id,))
            data = cursor.fetchone()
            print(f"Query result: {data}")
            
            return data

        except Exception as e:
            print(f"Database error: {e}")
            print(traceback.format_exc())
            return None
        finally:
            cursor.close()
            connection.close()
            print("Database connection closed")