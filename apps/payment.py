import dash_bootstrap_components as dbc
from dash import dcc, html, Output, Input, State, ALL
import pandas as pd
from dash.exceptions import PreventUpdate
from apps.dbconnect import create_connection, close_connection
import json
import dash

def fetch_data(patient_name=None, appointment_date=None, doctor_name=None, payment_method=None, payment_status=None):
    connection = create_connection()
    
    try:
        cursor = connection.cursor(dictionary=True)
        
        query = """
            SELECT DISTINCT
                p.patient_id, 
                p.patient_first_name, 
                p.patient_last_name,
                a.appointment_date, 
                py.payment_method, 
                py.payment_status, 
                py.payment_amount,
                d.doctor_name
            FROM patient p
            JOIN appointment a ON p.patient_id = a.patient_id
            JOIN payment py ON p.patient_id = py.patient_id
            JOIN doctor d ON a.doctor_id = d.doctor_id
            WHERE 1=1
        """
        
        params = []
        
        # Add filter conditions
        if patient_name:
            query += """ AND CONCAT(p.patient_first_name, ' ', p.patient_last_name) 
                        LIKE %s"""
            params.append(f"%{patient_name}%")
            
        if appointment_date:
            query += " AND DATE(a.appointment_date) = %s"
            params.append(appointment_date)
            
        if doctor_name:
            query += " AND d.doctor_name LIKE %s"
            params.append(f"%{doctor_name}%")
            
        if payment_method:
            query += " AND py.payment_method = %s"
            params.append(payment_method)
            
        if payment_status:
            query += " AND py.payment_status = %s"
            params.append(payment_status)
            
        print(f"Executing query with parameters: {params}")
        
        cursor.execute(query, tuple(params))
        result = cursor.fetchall()
        
        print(f"Number of records fetched: {len(result)}")
        return result
        
    except Exception as e:
        print(f"Error in fetch_data: {e}")
        print(f"Query that caused error: {query}")
        print(f"Parameters: {params}")
        return []
        
    finally:
        if 'cursor' in locals():
            cursor.close()
        close_connection(connection)

# Get unique values for dropdowns
def get_patient_names():
    # Query to get unique patient names
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT DISTINCT 
                patient_id,
                CONCAT(patient_first_name, ' ', patient_last_name) as full_name 
            FROM patient
            ORDER BY full_name
        """)
        return [{'label': row['full_name'], 'value': row['full_name']} for row in cursor.fetchall()]
    finally:
        cursor.close()
        connection.close()

def get_doctor_names():
    # Query to get unique doctor names
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute("SELECT DISTINCT doctor_name FROM doctor ORDER BY doctor_name")
        return [{'label': row['doctor_name'], 'value': row['doctor_name']} for row in cursor.fetchall()]
    finally:
        cursor.close()
        connection.close()

def delete_record(patient_id):
    """
    Deletes a patient record and all related records from the database.
    
    Args:
        patient_id (int): The ID of the patient to delete
        
    Returns:
        bool: True if deletion was successful, False otherwise
    """
    connection = create_connection()
    cursor = None
    try:
        cursor = connection.cursor()
        
        # Start transaction
        connection.start_transaction()
        
        print(f"Starting deletion process for patient_id: {patient_id}")
        
        # Check if patient exists
        cursor.execute("SELECT patient_id FROM patient WHERE patient_id = %s", (patient_id,))
        if not cursor.fetchone():
            print(f"No patient found with ID: {patient_id}")
            connection.rollback()
            return False

        try:
            # 1. First delete from medical_record table
            cursor.execute("""
                DELETE FROM medical_record 
                WHERE patient_id = %s
            """, (patient_id,))
            medical_records_deleted = cursor.rowcount
            print(f"Deleted {medical_records_deleted} medical records for patient_id: {patient_id}")

            # 2. Delete from appointment table
            cursor.execute("""
                DELETE FROM appointment 
                WHERE patient_id = %s
            """, (patient_id,))
            appointments_deleted = cursor.rowcount
            print(f"Deleted {appointments_deleted} appointments for patient_id: {patient_id}")

            # 3. Delete from payment table
            cursor.execute("""
                DELETE FROM payment 
                WHERE patient_id = %s
            """, (patient_id,))
            payments_deleted = cursor.rowcount
            print(f"Deleted {payments_deleted} payments for patient_id: {patient_id}")
            
            # 4. Finally delete the patient record
            cursor.execute("""
                DELETE FROM patient 
                WHERE patient_id = %s
            """, (patient_id,))
            patient_deleted = cursor.rowcount
            print(f"Deleted {patient_deleted} patient record for patient_id: {patient_id}")
            
            # Commit transaction
            connection.commit()
            print(f"Successfully deleted patient {patient_id} and all related records")
            return True
            
        except Exception as e:
            print(f"Error during delete operations: {str(e)}")
            connection.rollback()
            return False
            
    except Exception as e:
        print(f"Error establishing database connection or transaction: {str(e)}")
        if connection:
            connection.rollback()
        return False
        
    finally:
        if cursor:
            cursor.close()
        if connection:
            try:
                connection.close()
                print("Database connection closed.")
            except Exception as e:
                print(f"Error closing connection: {str(e)}")

# Define the updated table headers
headers = ["ID", "Patient Name", "Appointment Date", "Payment Method", "Doctor Name", "Payment Status", "Amount (in Php)", "Edit", "Delete"]

# Define styles for the layout 
styles = {
    "subHeader1": {
        "padding": "40px",
        "marginLeft": "60px"
    },
    "paymentRecord": {
        "fontSize": "30px",
        "color": "#05066d",
        "fontWeight": "bold"
    },
    "divider1": {
        "width": "93%",
        "border": "2px solid #05066d",
        "marginTop": "-3px"
    },
    "divider2": {
        "width": "93%",
        "border": "2px solid #05066d",
        "marginTop": "-30px"
    },
    "paymentRecords": {
        "fontSize": "18px",
        "color": "#05066d"
    },
}

# Set up routing and layout
layout = html.Div(
    children=[

        # Content 1
        html.Div(
            style=styles["subHeader1"],
            children=[
                # Section 1
                html.H2("Payment Records", style=styles["paymentRecord"]),
                html.Hr(style=styles["divider1"]),
                    dcc.Link(
                        html.Button(
                            'Add New Payment',
                            id='add-payment-button',
                            n_clicks=0,
                            style={
                                'backgroundColor': '#b0c5ff',
                                'color': '#05066d',
                                'fontSize': '14px',
                                'fontWeight': 'bold',
                                'padding': '5px 30px',
                                'border': '1px solid',
                                'borderRadius': '5px',
                                'cursor': 'pointer',
                                'boxShadow': '0px 4px 6px rgba(0, 0, 0, 0.1)',
                                'transition': 'background-color 0.3s ease'
                            }
                        ),
                        href='/add_new_payment'  # Link target to the "Add New Payment" page
                    ),
            ],
        ),

# The table - Payment Record
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
                        "margin-top": "-40px",  
                        "border": "1px solid black", 
                        "border-collapse": "collapse", 
                    },
                    children=[
                        # Table Header Row
                        html.Tr(
                            children=[
                                html.Th(
                                    children=[
                                        "Search Payment Records",
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
                                                        dcc.Dropdown(
                                                            id="patient-full-name-filter",
                                                            placeholder="Select patient",
                                                            options=get_patient_names(),
                                                            value=9,
                                                            style={"width": "250px", "font-style": "italic"}
                                                        ),
                                                    ],
                                                    style={"margin-right": "20px", "text-align": "left"},  # Spacing and alignment
                                                ),
                                                # Patient Appointment
                                                html.Div(
                                                    children=[
                                                        "Appointment Date",
                                                        html.Br(),  # Line break
                                                        dcc.DatePickerSingle(
                                                            id="date-picker-appoint",
                                                            placeholder="mm/dd/yyyy",  # Placeholder format
                                                            display_format="MM/DD/YYYY",  # Display format
                                                            style={
                                                                "margin-right": "183px",
                                                                "margin-bottom": "10px",  # Adjusted margin for bottom spacing
                                                                "width": "100px",  # Set width to 100px
                                                            },
                                                            className="custom-date-picker"  # Add a custom class for specific targeting
                                                        ),
                                                    ],
                                                    style={"text-align": "left"},  # Alignment
                                                ),

                                                 # Doctor Name
                                                html.Div([
                                                    html.Label("Doctor Name:"),
                                                    dcc.Dropdown(
                                                        id='doctor-name-input-filter',
                                                        options=get_doctor_names(),
                                                        placeholder="Select doctor name...",
                                                        style={'width': '300px'}
                                                    ),
                                                ], style={'margin': '10px'}),
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
                                                        html.Br(),  # Line break
                                                        dcc.RadioItems(
                                                            id="pay-method-radio-filter",  # ID for the RadioItems
                                                            options=[
                                                                {"label": "Cash", "value": "cash"},
                                                                {"label": "Gcash", "value": "gcash"},
                                                            ],
                                                            style={
                                                                "width": "250px",
                                                                "margin-right": "20px",
                                                                "padding": "2px",
                                                                "font-style": "italic"
                                                            },  # RadioItems container style
                                                            labelStyle={"display": "inline-block", "margin-right": "15px"},  # Inline style for radio options
                                                        ),
                                                    ],
                                                    style={"margin-right": "20px", "text-align": "left"},  # Spacing and alignment
                                                ),
                                                # Payment status
                                                html.Div(
                                                    children=[
                                                        "Payment Status",
                                                        html.Br(),  # Line break
                                                        dcc.RadioItems(
                                                            id="payment-radio-filter",  # ID for the RadioItems
                                                            options=[
                                                                {"label": "Paid", "value": "paid"},
                                                                {"label": "Not Yet Paid", "value": "not yet paid"},
                                                            ],
                                                            style={
                                                                "width": "250px",
                                                                "margin-right": "20px",
                                                                "padding": "2px",
                                                                "font-style": "italic"
                                                            },  # RadioItems container style
                                                            labelStyle={"display": "inline-block", "margin-right": "15px"},  # Inline style for radio options
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

        # Content 2
        html.Div(
            style=styles["subHeader1"],
            children=[

                # Section 2
                html.Hr(style=styles["divider2"]),
                html.H3("Payment Records", style=styles["paymentRecords"]),
            ],
        ),
        # Table for Payment History List
        html.Div(
        style={"padding": "0px"},
        children=[
        # Interval to trigger automatic updates
        dcc.Interval(
            id="interval-refresh",
            interval=1 * 1000,  # Trigger every 1 second
            n_intervals=0  # Start counting from 0
        ),

        html.Div(
            style={"padding": "10px"},
            children=[
                # Table Container
                html.Table(
                    style={
                        "width": "85%",
                        "margin-left": "88px",
                        "margin-right": "auto",
                        "margin-top": "-40px",
                        "border": "1px solid black",
                        "border-collapse": "collapse",
                    },
                    children=[
                        # Table Header
                        html.Tr(
                            children=[
                                html.Th(
                                    header,
                                    style={
                                        "padding": "12px",
                                        "text-align": "center",
                                        "font-weight": "bold",
                                        "background-color": "#05066d",
                                        "color": "white",
                                        "border": "1px solid black",
                                        "width": f"{100 / len(headers)}%",
                                    },
                                ) for header in headers
                            ],
                        ),
                        # Table Body: Dynamically populate rows from database data
                        html.Tbody(id="payment-history-table-body")
                    ],
                ),
            ],
        ),
    ],
),
html.Div(id="delete-status-message", style={"color": "green", "margin-top": "10px"}),
    ]
)

def payment_history_display(app):
    @app.callback(
        [Output("payment-history-table-body", "children", allow_duplicate=True),
         Output("delete-status-message", "children")],
        [Input({"type": "delete-button", "index": ALL}, "n_clicks")],
        [State({"type": "delete-button", "index": ALL}, "id")],
        prevent_initial_call=True
    )
    def handle_delete(n_clicks, ids):
        ctx = dash.callback_context
        if not ctx.triggered:
            raise PreventUpdate
            
        # Check if any delete button was actually clicked
        if not any(click is not None for click in n_clicks):
            raise PreventUpdate

        # Find which button was clicked
        triggered_input = ctx.triggered[0]
        button_id_str = triggered_input["prop_id"].split(".")[0]

        if "{" not in button_id_str:  # Not a delete button
            raise PreventUpdate

        try:
            button_id_dict = json.loads(button_id_str)
            if button_id_dict.get("type") != "delete-button":
                raise PreventUpdate

            patient_id = button_id_dict["index"]
            button_index = ids.index(button_id_dict)

            # Check if this specific button was clicked
            if n_clicks[button_index] is None:
                raise PreventUpdate

            print(f"Attempting to delete patient_id: {patient_id}")
            success = delete_record(patient_id)
            
            if success:
                print(f"Successfully deleted patient_id: {patient_id}")
                # Return empty filters to refresh the table
                records = fetch_data(
                    patient_name="",
                    appointment_date=None,
                    doctor_name="",
                    payment_method="",
                    payment_status=""
                )
                
                new_table_data = generate_table_rows(records)
                return new_table_data, f"Record with patient_id {patient_id} deleted successfully."
            else:
                print(f"Failed to delete patient_id: {patient_id}")
                return dash.no_update, f"Failed to delete record with patient_id {patient_id}."
                
        except Exception as e:
            error_msg = f"Error processing delete request: {str(e)}"
            print(error_msg)
            return dash.no_update, error_msg

    @app.callback(
        Output("payment-history-table-body", "children"),
        [Input("patient-full-name-filter", "value"),
         Input("date-picker-appoint", "date"),
         Input("doctor-name-input-filter", "value"),
         Input("pay-method-radio-filter", "value"),
         Input("payment-radio-filter", "value")]
    )
    def update_table(patient_name, appointment_date, doctor_name, payment_method, payment_status):
        try:
            records = fetch_data(
                patient_name=patient_name,
                appointment_date=appointment_date,
                doctor_name=doctor_name,
                payment_method=payment_method,
                payment_status=payment_status
            )
            
            return generate_table_rows(records)
            
        except Exception as e:
            print(f"Error in update table callback: {e}")
            return [html.Tr([html.Td(f"Error loading data: {str(e)}", 
                colSpan=8, style={"text-align": "center", "padding": "10px"})])]

def generate_table_rows(records):
    if not records:
        return [html.Tr([html.Td("No records found matching the filters", colSpan=8, 
            style={"text-align": "center", "padding": "10px"})])]
    
    # Common styles
    cell_style = {
        "text-align": "center",
        "padding": "10px",
        "border": "1px solid black"
    }
    
    button_style = {
        "margin": "2px",
        "padding": "5px 10px",
        "border": "none",
        "border-radius": "4px",
        "cursor": "pointer"
    }
    
    edit_button_style = {
        **button_style,
        "background-color": "#b0c5ff",
        "color": "#05066d",
    }
    
    delete_button_style = {
        **button_style,
        "background-color": "#f44336",
        "color": "white",
    }
    
    rows = []
    for record in records:
        try:
            payment_amount = f"₱{float(record['payment_amount']):,.2f}" if record['payment_amount'] else "N/A"
            appointment_date = record['appointment_date'].strftime('%Y-%m-%d') if record['appointment_date'] else "N/A"
            
            action_edit_buttons = html.Td([
                html.A(
                    html.Button(
                        "Edit",
                        id={'type': 'edit-button', 'index': record['patient_id']},
                        style=edit_button_style
                    ),
                    href=f"/edit_payment_mode/{record['patient_id']}", 
                ),
            ], style=cell_style)
            
            action_delete_buttons = html.Td([
                html.Button(
                    "Delete",
                    id={'type': 'delete-button', 'index': record['patient_id']},
                    style=delete_button_style
                ),
            ], style=cell_style)
            
            row = html.Tr([
                html.Td(record['patient_id'], style=cell_style),
                html.Td(
                    f"{record['patient_first_name']} {record['patient_last_name']}", 
                    style=cell_style
                ),
                html.Td(appointment_date, style=cell_style),
                html.Td(record['payment_method'], style=cell_style),
                html.Td(record['doctor_name'], style=cell_style),
                html.Td(record['payment_status'], style=cell_style),
                html.Td(payment_amount, style=cell_style),
                action_edit_buttons,
                action_delete_buttons
            ])
            rows.append(row)
        except KeyError as e:
            print(f"Error processing record - missing key: {e}")
            print(f"Record causing error: {record}")
            continue
            
    return rows