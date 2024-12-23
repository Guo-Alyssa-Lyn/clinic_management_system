from dash import html
from dash import dcc

# Define the styles for the navigation header
styles = {
    "headerLogin": {
        "display": "flex",
        "justifyContent": "space-between",
        "alignItems": "center",
        "backgroundColor": "white",
        "padding": "0px",
        "color": "#05066d",
    },
    "schedule": {
        "fontSize": "16px",
        "fontWeight": "normal",
        "color": "#05066d",
        "marginLeft": "20px",  
        "paddingTop": "10px",
    },
    "contactNumber": {
        "fontSize": "16px",
        "color": "#05066d",
        "paddingTop": "10px",
        "marginLeft": "20px",
    },
    "profileUser": {
        "fontSize": "15px",
        "color": "#05066d",
        "padding": "10px 20px",
        "textDecoration": "none",
        "marginLeft": "auto",
        "fontWeight": "bold",
    },
    "signOut": {
        "fontSize": "15px",
        "color": "#05066d",
        "padding": "10px 20px",
        "textDecoration": "none", 
        "fontWeight": "bold",
    },
}

# Define the navigation bar component
def generate_navbar():
    return html.Div([
        html.Div(
            style=styles["headerLogin"],
            children=[
                html.P("Mon - Sat at 9 AM to 5 PM", style=styles["schedule"]),
                html.P("(+63) 917 123 4567", style=styles["contactNumber"]),
                html.A(
                    [
                        html.Img(
                            src="/assets/resources/profile.jpg", 
                            style={"width": "13px", "height": "15px", "margin-right": "8px", "margin-bottom": "3px", "vertical-align": "middle"},
                        ),
                        "CLINIC TEAM"
                    ],
                    href="/clinic_employee",
                    style=styles["profileUser"],
                ),
                html.A("SIGN OUT", href="/login_page", style=styles["signOut"]),
            ],
        ),
        
        html.Div(
            className="header",
            children=[
                html.Div(
                    children=[
                        html.Img(
                            src="/assets/resources/Tumbocon Logo.png", 
                            alt="Tumbocon Polycare Clinic Logo", 
                            className="logo"
                        ),
                        html.Div("Tumbocon Polycare Clinic", className="title"),
                    ],
                    className="title-container"
                ),
                html.Div(
                    className="navLinks",
                    children=[
                        dcc.Link("Home", href="/home", className="link"),
                        dcc.Link("Medical Services", href="/medical_services", className="link"),
                        dcc.Link("Patient", href="/patient", className="link"),
                        dcc.Link("Payment", href="/payment", className="link"),
                        dcc.Link("Appointment", href="/appointment", className="linkLast"),
                    ],
                ),
            ]
        ),
    ])
