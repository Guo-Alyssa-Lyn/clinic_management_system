import os
import logging
from dash import Dash
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html, Input, Output

from apps import (
    home, payment, medical_services, patient_information,
    book_appointment, add_med_services, edit_medical_services,
    add_payment, edit_payment, medical_records, doctor_schedule, add_patient_information, 
    view_patient_medical_records, view_more_patient_med_records, 
    view_patient_edit_more_med_record, view_patient_add_more_med_record, 
    view_patient_patient_information, edit_patient_information, add_appointment,
    edit_appointment, add_doctor, edit_doctor, clinic_team, add_employee, edit_medical_records
)

import login_page

from apps.navbar import generate_navbar  # Import navbar from the navbar.py

# Initialize the Dash app
app = Dash(
    __name__, 
    suppress_callback_exceptions=True, 
    external_stylesheets=[dbc.themes.BOOTSTRAP, "/assets/customcss.css"],
    prevent_initial_callbacks=True  # Add this line to prevent initial duplicate callback calls
)

# Access Flask server
server = app.server

# Set the secret key for Flask sessions
server.secret_key = os.getenv('SECRET_KEY', 'your-default-secret-key')  # Use an environment variable or fallback

# Define the app layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='payment-status-message', style={'display': 'none'}),  # Hidden fallback
    dcc.Input(id='amount-input', type='number', value=0, style={'display': 'none'}),  # Hidden fallback for amount-input
    dcc.Dropdown(
    id='patient-full-name',  # Ensure this id is correctly referenced in your callback
    options=[],  # Initially empty; will be populated by the callback
    value=None,  # Default value
    placeholder="Select patient",
    style={'display': 'none'}  # Initially hidden
    ),
    dcc.Input(
            id='doctor-name-input',
            type='text',
            placeholder="Enter doctor name",
            style={'display': 'none'}  # Initially hidden
        ),
    dcc.Input(
            id="civil-status-input-edit",  # ID for the input field
            type="text",  # Type of the input field (text)
            placeholder="Single",  # Placeholder text for the input
            style={'display': 'none'}  # Initially hidden
                                                        ),
    dcc.Input(
            id="first-name-input-edit",  # ID for the input field
            type="text",  # Type of the input field (text)
            placeholder="Juan",  # Placeholder text for the input
            style={'display': 'none'}  # Initially hidden
                                                        ),
    dcc.Input(
            id="last-name-input-edit",  # ID for the input field
            type="text",  # Type of the input field (text)
            placeholder="Dela Cruz",  # Placeholder text for the input
            style={'display': 'none'}  # Initially hidden
                                                        ),
    html.Div(
            dcc.DatePickerSingle(
                id="birthday-picker-edit",
                placeholder="mm/dd/yyyy",  # Placeholder format
                display_format="MM/DD/YYYY",  # Display format
                style={
                    "margin-right": "150px",
                    "margin-bottom": "10px",  # Adjusted margin for bottom spacing
                    "width": "100px",  # Set width to 100px
                },
                className="custom-date-picker",  # Add a custom class for specific targeting
            ),
            style={"display": "none"},  # Hides the DatePickerSingle component
        ),
    dcc.Input(
            id="age-input-edit",  # ID for the input field
            type="number",  # Type of the input field (text)
            placeholder="20",  # Placeholder text for the input
            style={'display': 'none'}  # Initially hidden
                                                        ),
    html.Div(
            children=[
                "Sex",
                html.Br(),  # Line break
                dcc.Dropdown(
                    id="gender-dropdown-edit",  # ID for the dropdown
                    options=[
                        {"label": "Female", "value": "Female"},
                        {"label": "Male", "value": "Male"},
                        {"label": "Others", "value": "Others"},
                    ],
                    placeholder="Select Gender",  # Placeholder text
                    style={
                        "width": "250px",
                        "padding": "2px",
                        "margin-right": "20px",
                        "font-style": "italic",
                    },  # Dropdown style
                ),
            ],
            style={"display": "none", "text-align": "left"},  # Hidden and aligned left
        ),
    dcc.Input(
            id="contact-input-edit",  # ID for the input field
            type="number",  # Type of the input field (text)
            placeholder="0927 123 4567",  # Placeholder text for the input
            style={'display': 'none'}  # Initially hidden
                                                            ),
    dcc.Input(
            id="occupation-input-edit",  # ID for the input field
            type="text",  # Type of the input field (text)
            placeholder="student",  # Placeholder text for the input
            style={'display': 'none'}  # Initially hidden
                                                        ),
    dcc.Input(
            id="address-input-edit",  # ID for the input field
            type="text",  # Type of the input field (text)
            placeholder="123 Roxas Ave, Diliman, Quezon City",  # Placeholder text for the input
            style={'display': 'none'}  # Initially hidden
                                                            ),
    dcc.RadioItems(
    id="payment-method-radio",
    options=[
        {"label": "Cash", "value": "Cash"},
        {"label": "Gcash", "value": "Gcash"},
    ],
    value="Unpaid",  # Default value to ensure no None issues
    style={
        "width": "250px",
        "margin-right": "20px",
    },
    labelStyle={
        "display": "none",
        "margin-right": "10px",
    },
    ),
    dcc.RadioItems(
    id="payment-status-radio",
    options=[
        {"label": "Paid", "value": "Paid"},
        {"label": "Unpaid", "value": "Unpaid"},
    ],
    value="Unpaid",  # Default value to ensure no None issues
    style={
        "width": "250px",
        "margin-right": "20px",
    },
    labelStyle={
        "display": "none",
        "margin-right": "10px",
    },
    ),
    html.Button(
    "Add",
    id="add-button",
    n_clicks=0,
    style={
        "background-color": "green", 
        "color": "white", 
        "font-size": "14px",
        "font-weight": "bold",
        "border-radius": "5px",
        "padding": "5px 40px",  
        "margin-top": "40px", 
        "border": "none", 
        "cursor": "pointer",
        "display": "none"  # Initially hidden
    }
    ),
    html.Div(
    id="submit-status-add-med-record-new",
    style={
        "margin-top": "20px",
        "display": "none"  # Initially hidden
    }
    ),
    dcc.DatePickerSingle(
    id="date-picker-visit-add-auto",
    placeholder="mm/dd/yyyy",  # Placeholder format
    display_format="MM/DD/YYYY",  # Display format
    style={
        "margin-right": "168px",
        "margin-bottom": "15px",  # Adjusted margin for bottom spacing
        "width": "100px",  # Set width to 100px
        "display": "none"  # Initially hidden
    },
    className="custom-date-picker"  # Add a custom class for specific targeting
    ),
    dcc.Input(
    id="height-input-add",  # ID for the input field
    type="number",  # Type of the input field (number)
    placeholder="160",  # Placeholder text for the input
    style={
        "width": "100px", 
        "padding": "5px", 
        "margin-bottom": "50px", 
        "margin-right": "50px", 
        "font-style": "italic", 
        "display": "none"  # Initially hidden
    }  # Input style
    ),
    dcc.Input(
    id="weight-input-add",  # ID for the input field
    type="number",  # Type of the input field (number)
    placeholder="160",  # Placeholder text for the input
    style={
        "width": "100px", 
        "padding": "5px", 
        "margin-right": "50px", 
        "font-style": "italic", 
        "display": "none"  # Initially hidden
    }  # Input style
    ),
    dcc.Input(
    id="blood-pressure-input-add",  # ID for the input field
    type="text",  # Type of the input field (text)
    placeholder="120/80",  # Placeholder text for the input
    style={
        "width": "100px", 
        "padding": "5px", 
        "margin-right": "50px", 
        "font-style": "italic", 
        "display": "none"  # Initially hidden
    }  # Input style
    ),
    dcc.Input(
    id="temp-input-add",  # ID for the input field
    type="number",  # Type of the input field (number)
    placeholder="38",  # Placeholder text for the input
    style={
        "width": "100px", 
        "padding": "5px", 
        "margin-right": "50px", 
        "font-style": "italic", 
        "display": "none"  # Initially hidden
    }  # Input style
    ),
    dcc.Input(
    id="consult-type-input-add",  # ID for the input field
    type="text",  # Type of the input field (text)
    placeholder="Lorem ipsum",  # Placeholder text for the input
    style={
        "width": "250px", 
        "padding": "5px", 
        "margin-right": "30px", 
        "font-style": "italic", 
        "display": "none"  # Initially hidden
    }  # Input style
    ),
    dcc.Input(
    id="diagnosis-input-add",  # ID for the input field
    type="text",  # Type of the input field (text)
    placeholder="Lorem ipsum",  # Placeholder text for the input
    style={
        "width": "250px", 
        "padding": "5px", 
        "font-style": "italic", 
        "display": "none"  # Initially hidden
    }  # Input style
    ),
    dcc.Input(
    id="treatment-input-add",  # ID for the input field
    type="text",  # Type of the input field (text)
    placeholder="Lorem ipsum",  # Placeholder text for the input
    style={
        "width": "250px", 
        "margin-right": "20px", 
        "padding": "5px", 
        "font-style": "italic", 
        "display": "none"  # Initially hidden
    }  # Input style
    ),
    dcc.Input(
    id="lab-res-input-add",  # ID for the input field
    type="text",  # Type of the input field (text)
    placeholder="Lorem ipsum",  # Placeholder text for the input
    style={
        "width": "250px", 
        "padding": "5px", 
        "margin-right": "30px", 
        "font-style": "italic", 
        "display": "none"  # Initially hidden
    }  # Input style
    ),
    dcc.Input(
    id="note-input-add",  # ID for the input field
    type="text",  # Type of the input field (text)
    placeholder="Lorem ipsum",  # Placeholder text for the input
    style={
        "width": "250px", 
        "padding": "5px", 
        "font-style": "italic", 
        "display": "none"  # Initially hidden
    }  # Input style
    ),
    dcc.Dropdown(
    id="doctor-name-dropdown",
    options=[
        {"label": "Tony Jarvis", "value": "Tony Jarvis"},
    ],
    placeholder="Select a Doctor",
    style={
        "width": "250px",
        "padding": "5px",
        "font-style": "italic",
        "display": "none",  # Initially hidden
    },
    ),
    dcc.Dropdown(
        id='doctor-id',  # Ensure the ID is correct
        options=[],  # Initially empty, will be populated by callback
        value='default_value',  # A default value if necessary
        style={'display': 'none'}  # Initially hidden
    ),
    html.Button(
    id="add-button-payment",
    children="Add Payment",
    n_clicks=0,  # Initialize the click count
    style={"display": "none"},  # Initially hidden
    ),
    dcc.DatePickerSingle(
    id="date-picker-appoint",
    style={"display": "none"},  # Initially hidden
    placeholder="Select a date",  # Optional placeholder
    ),
    html.Div(
    id="appointment-date-error",
    children="",  # Initially empty
    style={"display": "none", "color": "red"},  # Hidden and styled
    ),
    html.Div(
        dcc.DatePickerSingle(
            id='date-picker-appoint-edit-mode',
        ),
        style={'display': 'none'}
    ),
    html.Div(
        dcc.Input(
            id='full-name-input-edit-mode',
            type='text',
            value='',
            placeholder='Enter full name',
        ),
        style={'display': 'none'}
    ),
    html.Div(
        dcc.Input(
            id='time-input-edit-mode',
            type='text',  # Set the type to 'time'
            value='',     # Initial value can be set if needed
            placeholder='Enter time',
        ),
        style={'display': 'none'}  # Initially hidden
    ),
    html.Div(
        dcc.Input(
            id='contact-input-edit-mode',
            type='number',   # Set type based on your requirements (e.g., 'text' or 'tel')
            value='',      # Initial value, if any
            placeholder='Enter contact information',
        ),
        style={'display': 'none'}  # Initially hidden
    ),
    dcc.DatePickerSingle(
        id='date-picker-appointment-modify',
        date='2024-12-22',  # You can set a default date if needed
        style={'display': 'none'}  # Initially hidden
    ),
    dcc.Input(
        id='doctor-name-input-modify', 
        type='text', 
        value='', 
        style={'display': 'none'}  # Initially hidden
    ),
    dcc.Dropdown(
        id='payment-method-modify',
        options=[
            {'label': 'Credit Card', 'value': 'credit_card'},
            {'label': 'PayPal', 'value': 'paypal'},
            {'label': 'Bank Transfer', 'value': 'bank_transfer'}
        ],
        value=None,
        style={'display': 'none'}  # Initially hidden
    ),
    dcc.Dropdown(
        id='payment-status-modify',
        options=[
            {'label': 'Pending', 'value': 'pending'},
            {'label': 'Completed', 'value': 'completed'},
            {'label': 'Failed', 'value': 'failed'}
        ],
        value=None,
        style={'display': 'none'}  # Initially hidden
    ),
    dcc.Input(
        id='amount-input-modify',
        type='number',
        value='',
        style={'display': 'none'}  # Initially hidden
    ),
    dcc.Input(
        id="fullname-input-modify",
        type="text",
        placeholder="Enter your name",
        style={"display": "none"}  # Initially hidden
    ),
    dcc.Input(id='full-name-input-modify', type='text', value='', style={'display': 'none'}), 
    html.Div(id="page-load-trigger"),
    html.Div(id='add-med-record-link'),
    html.Div(id='patient-records'),
    dcc.Store(id='service-data-store'), 
    dcc.Store(id='patient-data-store'), 
    dcc.Store(id='doctor-data-store'), 
    dcc.Store(id='medical-record-data-store'),
    dcc.Store(id='view-patient-info-data-store'),
    dcc.Store(id='medical-record-adding-data-store'),
    dcc.Store(id='view-patient-medical-records-data-store'),
    dcc.Store(id='edit-medical-record-mode-data-store'),
    dcc.Store(id='patient-id-payment'),
    dcc.Store(id='appointment-data-store', storage_type='memory'),
    dcc.Store(id='payment-edit-data-store', storage_type='memory'),
    dcc.Store(id="count-data-store"),
    html.Div(id='page-content'),
])

# Set app title that appears in your browser tab
app.title = 'Tumbocon Polycare Clinic'

@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    # Define the navigation bar only once
    navigation_bar = generate_navbar()

    # Submenu logic based on the current pathname
    submenu = None
    page_content = None

    if pathname == '/' or pathname == '/login_page':
        navigation_bar = None
        submenu = None
        page_content = login_page.layout(show_navbar=False)
    elif pathname == '/home':
        submenu = None
        page_content = home.layout
    elif pathname == '/payment':
        submenu = None
        page_content = payment.layout
    elif pathname == '/add_new_payment':
        submenu = None
        page_content = add_payment.layout
    elif pathname == '/medical_services':
        page_content = medical_services.layout
    elif pathname == '/patient':
        submenu = html.Div([  
            dcc.Link("Patient Information", href="/patient_information", className='submenu-link'),
            dcc.Link("Medical Records", href="/medical_records", className='submenu-link')
        ], className='submenu-container2')
        page_content = home.layout
    elif pathname == '/appointment':
        submenu = html.Div([  
            dcc.Link("Book an Appointment", href="/book_appointment", className='submenu-link'),
            dcc.Link("Doctor Schedule", href="/doctor_schedule", className='submenu-link')
        ], className='submenu-container1')
        page_content = home.layout
    elif pathname == '/patient_information':
        submenu = None
        page_content = patient_information.layout
    elif pathname == '/add_medical_services':
        submenu = None
        page_content = add_med_services.layout
    elif pathname == '/medical_records':
        submenu = None
        page_content = medical_records.layout
    elif pathname == '/edit_medical_services_page':
        submenu = None
        page_content = edit_medical_services.layout
    elif pathname == '/add_new_patient':
        submenu = None
        page_content = add_patient_information.layout
    elif pathname == '/edit_medical_records':
        submenu = None
        page_content = edit_medical_records.layout
    elif pathname == '/view_patient_medical_records': 
        submenu = None
        page_content = view_patient_medical_records.layout  # Just return the layout here
    elif pathname.startswith('/view_patient_medical_records/'):  # Dynamic route for patient medical records
        # Extract patient_id from the URL
        patient_id = pathname.split('/')[-1]
        # Pass the patient_id to the layout
        page_content = view_patient_medical_records.layout
    elif pathname == '/view_patient_more_medical_record':
        submenu = None
        page_content = view_more_patient_med_records.layout
    elif pathname == '/edit_patient_more_medical_records':
        submenu = None
        page_content = view_patient_edit_more_med_record.layout
    elif pathname.startswith('/edit_patient_more_medical_records/'):  # Dynamic route for patient medical records
        # Extract patient_id from the URL
        patient_id = pathname.split('/')[-1]
        # Pass the patient_id to the layout
        page_content = view_patient_edit_more_med_record.layout
    elif pathname.startswith('/view_medical_records_history/'):  # Dynamic route for patient medical records
        # Extract patient_id from the URL
        patient_id = pathname.split('/')[-1]
        # Pass the patient_id to the layout
        page_content = view_more_patient_med_records.layout
    elif pathname == '/view_patient_add_medical_record':  
        submenu = None
        page_content = view_patient_add_more_med_record.layout  
    elif pathname.startswith('/view_patient_add_medical_record'):
        # Extract patient_id from the URL
        patient_id = pathname.split('/')[-1]
        
        # Pass the patient_id to the layout for the "add medical record" page
        submenu = None
        page_content = view_patient_add_more_med_record.layout
    elif pathname == '/view_patient_information': 
        submenu = None
        page_content = view_patient_patient_information.layout
    elif pathname == '/edit_patient_information':
        submenu = None
        page_content = edit_patient_information.layout
    elif pathname == '/book_appointment':
        submenu = None
        page_content = book_appointment.layout
    elif pathname == '/add_appointment':
        submenu = None
        page_content = add_appointment.layout
    elif pathname == '/edit_appointment':
        submenu = None
        page_content = edit_appointment.layout
    elif pathname == '/doctor_schedule':
        submenu = None
        page_content = doctor_schedule.layout
    elif pathname == '/add_doctor':
        submenu = None
        page_content = add_doctor.layout
    elif pathname == '/edit_doctor':
        submenu = None
        page_content = edit_doctor.layout
    elif pathname == '/clinic_employee':
        submenu = None
        page_content = clinic_team.layout
    elif pathname == '/add_employee':
        submenu = None
        page_content = add_employee.layout
    elif pathname == '/edit_payment_mode':
        submenu = None
        page_content = edit_payment.layout
    elif pathname.startswith('/edit_payment_mode'):
        # Extract patient_id from the URL
        patient_id = pathname.split('/')[-1]
       
        submenu = None
        page_content = edit_payment.layout
    else:
        submenu = None
        page_content = html.Div("404 Page Not Found", className="not-found")

    # Return the combined layout (navigation, submenu, and page content)
    return html.Div([
        navigation_bar,
        submenu,
        html.Div(page_content, className='page-content')
    ])

# Register callbacks for individual modules
add_patient_information.register_callbacks(app)
add_med_services.register_callbacks(app)
add_payment.payment_accept(app)
add_appointment.register_callbacks(app)
add_doctor.register_callbacks(app)
add_employee.register_callbacks(app)
medical_services.filter_search(app)
medical_records.medical_records_display(app)
clinic_team.clinic_employee_display(app)
doctor_schedule.doctor_schedule_display(app)
book_appointment.book_appointment_display(app)
view_patient_medical_records.view_patient(app)
login_page.accept_login_form(app)
patient_information.update_table_display(app)
payment.payment_history_display(app)
edit_medical_services.edit_mode(app)
edit_patient_information.edit_mode_info(app)
edit_doctor.edit_mode_doctor_sched(app)
edit_appointment.edit_mode_appointment(app)
edit_medical_records.edit_mode_medical_record(app)
view_patient_patient_information.view_patient_info_mode(app)
view_patient_add_more_med_record.add_medical_record_patient(app)
home.home_page_functions(app)
view_more_patient_med_records.view_mode_medical_records(app)
view_patient_edit_more_med_record.edit_medical_record_mode(app)
edit_payment.edit_mode_payment_details(app)

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)

# Reduce logs in the terminal
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
