import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, State
from dash.exceptions import PreventUpdate
from datetime import datetime
from apps.dbconnect import create_connection, close_connection

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

        # The table - Add New Payment
        # Adjusted styles for table box to maintain fixed positions
        html.Div(
    style={"padding": "0px"},
    children=[
        html.Div(
            style={"padding": "10px"},
            children=[
                # Table Container with fixed width and alignment
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
                                    children=["Add New Payment"],
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
                                                        html.Br(),
                                                        dcc.Dropdown(
                                                            id="patient-full-name",
                                                            placeholder="Select patient",
                                                            options=[
                                                                {'label': 'Patient 1', 'value': 1},
                                                            ],
                                                            value=9,
                                                            style={
                                                                "width": "250px",
                                                                "min-height": "40px",
                                                                "padding": "5px",
                                                            },
                                                        ),
                                                    ],
                                                    style={
                                                        "margin-right": "40px",
                                                        "text-align": "left",
                                                        "min-width": "300px",
                                                    },
                                                ),
                                                # Appointment Date
                                                html.Div(
                                                        children=[
                                                            "Appointment Date",
                                                            html.Br(),
                                                            dcc.DatePickerSingle(
                                                                id="date-picker-appoint",
                                                                placeholder="mm/dd/yyyy",
                                                                display_format="MM/DD/YYYY",
                                                                date=None,
                                                                style={
                                                                    "margin-right": "20px",
                                                                    "width": "250px",
                                                                },
                                                                className="custom-date-picker",
                                                            ),
                                                        ],
                                                        style={
                                                            "text-align": "left",
                                                            "min-width": "300px",
                                                        },
                                                    ),

                                                # Doctor Full Name
                                                # Modify the layout to include a dropdown for doctor selection
                                                html.Div(
                                                    children=[
                                                        "Doctor Name",
                                                        html.Br(),
                                                        dcc.Dropdown(
                                                            id="doctor-name-dropdown",  # Ensure the ID is consistent with the callback
                                                            placeholder="Select a Doctor",
                                                            options=[],  # Initially empty, will be populated by callback
                                                            style={
                                                                "width": "250px",
                                                                "padding": "5px",
                                                                "font-style": "italic",
                                                            },
                                                        ),
                                                        dcc.Dropdown(
                                                            id='doctor-id',  # Ensure the ID is correct
                                                            options=[],  # Initially empty, will be populated by callback
                                                            value='default_value',  # A default value if necessary
                                                            style={'display': 'none'}  # Initially hidden
                                                        ),
                                                    ],
                                                    style={
                                                        "margin-right": "20px",
                                                        "text-align": "left",
                                                        "min-width": "300px",
                                                    },
                                                ),
                                                
                                            ],
                                            style={
                                                "display": "flex",
                                                "gap": "20px",
                                                "align-items": "center",
                                                "flex-wrap": "nowrap",  # Prevents wrapping
                                                "justify-content": "flex-start",  # Align items to the left
                                            },
                                        ),
                                        # Second line input fields
                                        html.Div(
                                            children=[
                                                # Payment Method
                                                html.Div(
                                                    children=[
                                                        "Payment Method",
                                                        html.Br(),
                                                        dcc.RadioItems(
                                                            id="payment-method-radio",
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
                                                # Payment Status
                                                html.Div(
                                                    children=[
                                                        "Payment Method",
                                                        html.Br(),
                                                        dcc.RadioItems(
                                                            id="payment-status-radio",
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
                                                        html.Br(),
                                                        dcc.Input(
                                                            id="amount-input",
                                                            type="number",
                                                            placeholder="123.00",
                                                            style={
                                                                "width": "250px",
                                                                "padding": "5px",
                                                                "font-style": "italic",
                                                            },
                                                        ),
                                                    ],
                                                    style={
                                                        "text-align": "left",
                                                        "visibility": "visible",
                                                        "min-width": "300px",
                                                        "position": "relative",  # Keep its position fixed
                                                    },
                                                ),
                                            ],
                                            style={
                                                "display": "flex",
                                                "gap": "20px",
                                                "align-items": "center",
                                                "flex-wrap": "nowrap",  # Prevents wrapping
                                            },
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
                                                        href="/payment",  # Replace with the target URL
                                                    ),
                                                html.Button(
                                                    "Add",
                                                    id="add-button-payment",
                                                    n_clicks=0,
                                                    style={
                                                        "background-color": "#4CAF50",
                                                        "color": "white",
                                                        "border-radius": "5px",
                                                        "font-weight": "bold",
                                                        "font-size": "14px",
                                                        "padding": "5px 40px",
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
        html.Div(id='payment-status-message'),
        html.Div(id='appointment-date-error', className='error-message'),
    ]
)

def payment_accept(app):
    @app.callback(
        [Output('doctor-name-dropdown', 'options'),
         Output('patient-full-name', 'options'),
         Output('date-picker-appoint', 'date'),
         Output('appointment-date-error', 'children'),
         Output('payment-status-message', 'children'),
         Output('patient-full-name', 'value'),
         Output('doctor-name-dropdown', 'value'),
         Output('payment-method-radio', 'value'),
         Output('payment-status-radio', 'value'),
         Output('amount-input', 'value')],
        [Input('patient-full-name', 'value'),
         Input('add-button-payment', 'n_clicks')],
        [State('payment-method-radio', 'value'),
         State('payment-status-radio', 'value'),
         State('amount-input', 'value'),
         State('doctor-name-dropdown', 'value'),
         State('date-picker-appoint', 'date')]
    )
    def update_form(selected_patient_id, n_clicks,
                    payment_method, payment_status, amount, doctor_id, appointment_date):
        ctx = dash.callback_context
        trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

        # Initialize default returns
        doctor_options = []
        patient_options = []
        appt_date = None
        appt_error = ""
        status_message = ""
        patient_value = dash.no_update
        doctor_value = dash.no_update
        payment_method_value = dash.no_update
        payment_status_value = dash.no_update
        amount_value = dash.no_update

        try:
            conn = create_connection()
            cursor = conn.cursor()

            # Fetch doctors
            doctor_query = """
                SELECT doctor_id, doctor_name 
                FROM doctor 
                ORDER BY doctor_name
            """
            cursor.execute(doctor_query)
            doctor_data = cursor.fetchall()
            doctor_options = [{'label': name[1], 'value': name[0]} for name in doctor_data]

            # Fetch patients
            patient_query = """
                SELECT patient_id, CONCAT(patient_first_name, ' ', patient_last_name) as full_name 
                FROM patient 
                ORDER BY patient_first_name
            """
            cursor.execute(patient_query)
            patient_data = cursor.fetchall()
            patient_options = [{'label': name[1], 'value': name[0]} for name in patient_data]

            # Handle appointment date fetch when patient is selected
            if trigger_id == 'patient-full-name' and selected_patient_id:
                appt_query = """
                    SELECT appointment_date 
                    FROM appointment 
                    WHERE patient_id = %s 
                        AND payment_id IS NULL
                """
                cursor.execute(appt_query, (selected_patient_id,))
                result = cursor.fetchone()

                print("Fetched result:", result)  # Debugging

                if result and result[0]:
                    appt_date = result[0].strftime('%Y-%m-%d')  # Correct format for DatePickerSingle
                    print("Formatted appointment_date for DatePicker:", appt_date)  # Debugging
                else:
                    appt_date = None
                    appt_error = "No upcoming unpaid appointments found for this patient."

            # Handle payment submission
            if trigger_id == 'add-button-payment' and n_clicks:
                if not all([payment_method, payment_status, amount, selected_patient_id, doctor_id, appointment_date]):
                    status_message = "Please fill in all required fields."
                else:
                    try:
                        # If the connection has an active transaction, commit or rollback
                        conn.commit()  # Or conn.rollback() if you don't want to commit any changes

                        conn.start_transaction()  # Now start a new transaction

                        # Insert payment record
                        payment_date = datetime.now() if payment_status == 'Paid' else None
                        insert_payment_query = """
                            INSERT INTO payment (patient_id, payment_method, payment_status, payment_amount, payment_date)
                            VALUES (%s, %s, %s, %s, %s)
                        """
                        cursor.execute(insert_payment_query, (
                            selected_patient_id,
                            payment_method, 
                            payment_status, 
                            float(amount), 
                            payment_date
                        ))

                        payment_id = cursor.lastrowid

                        # Update appointment with payment_id
                        update_appointment_query = """
                            UPDATE appointment 
                            SET payment_id = %s,
                                doctor_id = %s
                            WHERE patient_id = %s 
                            AND appointment_date = %s
                        """
                        cursor.execute(update_appointment_query, (
                            payment_id,
                            doctor_id,
                            selected_patient_id,
                            appointment_date
                        ))

                        conn.commit()  # Commit the transaction after all operations
                        status_message = "Payment processed successfully!"

                        # Clear form values after successful submission
                        patient_value = None
                        doctor_value = None
                        payment_method_value = None
                        payment_status_value = None
                        amount_value = None

                    except Exception as err:
                        conn.rollback()
                        status_message = f"Error processing payment: {str(err)}"
                        print(f"Error in payment processing: {err}")

        except Exception as err:
            print(f"Database error: {err}")
            status_message = f"Database error: {str(err)}"

        finally:
            try:
                close_connection(conn)
            except:
                pass

        return (
            doctor_options,
            patient_options,
            appt_date,
            appt_error,
            status_message,
            patient_value,
            doctor_value,
            payment_method_value,
            payment_status_value,
            amount_value
        )