import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, State
from dash.exceptions import PreventUpdate
from flask import session
from apps.navbar import generate_navbar
from apps.dbconnect import create_connection, close_connection
import dash
import bcrypt

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
        "marginRight": "auto",
        "marginLeft": "20px"
    },
}

def layout(show_navbar=False):
# Define the layout
    return html.Div([
        generate_navbar() if show_navbar else None,
        # Header
        html.Div(
            style=styles["headerLogin"],
            children=[
                html.P("Mon - Sat at 9 AM to 5 PM", style=styles["schedule"]),
                html.P("(+63) 917 123 4567", style=styles["contactNumber"]),
            ],
        ),
        
        # Clinic Logo and Title
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
            ]
        ),
        
        # Login Form
        html.Div(
            style={
                "display": "flex",
                "justifyContent": "center",
                "alignItems": "center",
                "height": "50vh",
                "backgroundColor": "#f4f4f4",
            },
            children=[
                html.Div(
                    style={
                        "width": "400px",
                        "padding": "20px",
                        "marginTop": "140px",
                        "border": "1px solid #ccc",
                        "borderRadius": "5px",
                        "boxShadow": "0 4px 8px rgba(0, 0, 0, 0.1)",
                        "backgroundColor": "#05066d",
                    },
                    children=[
                        html.H2("User Login", style={"textAlign": "center", "marginBottom": "40px", "marginTop": "20px", "color": "white",}),
                        dcc.Input(
                            id="email",
                            type="text",
                            placeholder="Enter email",
                            style={
                                "width": "80%", 
                                "height": "20%",
                                "marginBottom": "20px",
                                "padding": "5px",
                                "borderRadius": "5px",
                                "border": "1px solid",
                                "display": "block",
                                "marginLeft": "auto",
                                "marginRight": "auto",
                            },
                        ),
                        dcc.Input(
                            id="password",
                            type="password",
                            placeholder="Enter password",
                            style={
                                "width": "80%", 
                                "height": "20%",
                                "marginBottom": "20px",
                                "padding": "5px",
                                "borderRadius": "5px",
                                "border": "1px solid",
                                "display": "block",
                                "marginLeft": "auto",
                                "marginRight": "auto",
                            },
                        ),
                        html.Button(
                            "Login",
                            id="login-button",
                            n_clicks=0,
                            style={
                                "width": "30%", 
                                "paddingTop": "5px",
                                "paddingBottom": "5px",
                                "backgroundColor": "#b0c5ff",
                                "color": "#3b365f",
                                "fontWeight": "bold",
                                "border": "none",
                                "borderRadius": "5px",
                                "cursor": "pointer",
                                "display": "block",
                                "marginLeft": "auto",
                                "marginRight": "auto",
                                "marginBottom": "40px"
                            },
                        ),
                        html.Div(id="login-message", style={"marginTop": "10px", "textAlign": "center", "color": "red"}),
                    ],
                )
            ],
        ),
    ])

def accept_login_form(app):
    # Callback to handle login
    @app.callback(
        [Output("login-message", "children"), Output("url", "pathname")],
        [Input("login-button", "n_clicks")],
        [State("email", "value"), State("password", "value")],
    )
    def login_user(n_clicks, email, password):
        if n_clicks > 0:
            if not email or not password:
                return "Please enter both email and password.", dash.no_update

            try:
                conn = create_connection()  # Use create_connection from dbconnect
                cursor = conn.cursor()

                # Query the database for the user
                query = "SELECT secretary_password FROM clinic_secretary WHERE secretary_email = %s"
                cursor.execute(query, (email,))
                result = cursor.fetchone()

                if result:
                    stored_password = result[0]

                    # Check password (assumes passwords in the database are hashed)
                    if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
                        session['user'] = email  # Set session variable (if using Flask sessions)
                        return html.Div("Login successful!", style={"color": "green"}), "/home"
                    else:
                        return "Invalid email or password.", dash.no_update
                else:
                    return "Invalid email or password.", dash.no_update

            except Exception as e:
                return f"An error occurred: {str(e)}", dash.no_update

            finally:
                cursor.close()
                close_connection(conn)  # Use close_connection from dbconnect

        raise PreventUpdate