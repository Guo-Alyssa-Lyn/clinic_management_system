# Usual Dash dependencies
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, State
from dash.exceptions import PreventUpdate

# Let us import the app object in case we need to define
# callbacks here
from app import app

navbar = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Img(src='/assets/resources/Time Icon.png', 
                                style={'width': 'auto', 
                                        'height': '2vh'}, 
                                className='pe-1'), #Picture
                        html.Div('Mon - Sat at 9AM to 5PM',
                                style={'fontSize': '2vh',
                                        'marginRight':'2.3vw'}, 
                                ),
                        html.Img(src='/assets/resources/Phone Icon.png', 
                                style={'width': 'auto', 
                                        'height': '2vh'}, 
                                className='pe-1'), #Picture
                        html.Div('(+63) 907 975 2173', 
                                style={'fontSize': '2vh',
                                        'marginRight':'2.3vw'}, 
                                ),
                        html.Img(src='/assets/resources/Place Icon.png', 
                                style={'width': 'auto', 
                                        'height': '2vh'}, 
                                className='pe-1'), #Picture
                        html.Div('44 Governor Pascual, Brgy. Concepcion, Malabon City', 
                                style={'fontSize': '2vh',
                                        'marginRight':'2.3vw'}, 
                                ),
                    ],
                    width=8, 
                    style={'display': 'flex', 
                        'align-items': 'center', 
                        'color': '#05066d'},
                    className='ms-4'
                ),
                
                dbc.Col(
                    [
                    html.Img(src='/assets/resources/profile.jpg', 
                                style={'width': 'auto', 
                                        'height': '2vh'}),
                    
                    dbc.Button('MY PROFILE', 
                            id='prof-btn', 
                            style={'backgroundColor': '#FFF', 
                                    'color': '#05066d', 
                                    'border': 'none', 
                                    'fontSize': '2vh',
                                    'fontWeight': 'Bold'}, 
                                className='ps-1'),
                    
                    html.Img(src='/assets/resources/Sign Out Icon.png', 
                                style={'width': 'auto', 
                                        'height': '2vh'}, 
                                className = 'ps-5'),
                    
                    dbc.Button('SIGN OUT', 
                            id='out-btn',  
                            style={'backgroundColor': '#FFF', 
                                    'color': '#05066d', 
                                    'border': 'none', 
                                    'fontSize': '2vh',
                                    'fontWeight': 'Bold'}, 
                                className = 'ps-1'),
                    ],
                    width=True,
                    style={'display': 'flex', 
                        'align-items': 'center', 
                        'justify-content': 'flex-end'},
                    className='me-3'
                ),
            ],
            align='center',
            justify='between',
            style={'background-color': '#FFF',
                'width': '100%'},
            className='py-1'
        ),

        dbc.Navbar(
                dbc.Container(
                    [
                        html.A(
                            dbc.Row(
                                [
                                    dbc.Col([
                                        html.Img(src='/assets/resources/Tumbocon Logo.png', 
                                                style={'width': 'auto', 
                                                    'height': '7vh'}),
                                    ]),
                                    dbc.Col(
                                        dbc.NavbarBrand("Tumbocon Polycare Clinic", 
                                                            style={'fontSize':'4vh', 
                                                                   'fontFamily':'Segoe UI', 
                                                                   'fontWeight':'Bold', 
                                                                   'color': '#004bad'}, 
                                                            className="ms-2")
                                    ),
                                ],
                                align="center",
                                className='g-0 me-4'
                            ),
                            href="/home",
                            style={'textDecoration': 'none'}
                        ),
                        dbc.NavLink("HOME", 
                                    href="/home"),
                        dbc.NavLink("MEDICAL SERVICES", 
                                    href="medical_services"),
                        dbc.DropdownMenu(
                                        [
                                        dbc.DropdownMenuItem('Patient Information', 
                                                             href='/patient_information', style={'backgroundColor':'#FFF', 'color':'#05066d'}),
                                        dbc.DropdownMenuItem('Medical Records', 
                                                             href='/medical_records', style={'backgroundColor':'#FFF', 'color':'#05066d'}),
                                        ],
                                    nav=True,
                                    in_navbar=True,
                                    label='PATIENT',
                                    className='dropdown-hover' 'mx-5',
                                    ),
                        dbc.NavLink("PAYMENT", 
                                    href="/payment"),
                        dbc.DropdownMenu(
                                        [
                                        dbc.DropdownMenuItem('Book An Appointment', 
                                                             href='/appointment_booking', style={'backgroundColor':'#FFF', 'color':'#05066d'}),
                                        dbc.DropdownMenuItem('Doctor Schedule', 
                                                             href='/doctor_schedule', style={'backgroundColor':'#FFF', 'color':'#05066d'}),
                                        ],
                                    style={},
                                    nav=True,
                                    in_navbar=True,
                                    label='APPOINTMENT',
                                    className='dropdown-hover p-0 m-0',
                                    
                                    ),
                    ], className='m-0 justify-content py-3', 
                        style={'fontSize':'2.5vh', 
                               'fontFamily':'Segoe UI', 
                               'color': '#05066d' }
                    
                ),  light=True,
                    color='#b0c5ff'
        )
    ]
)