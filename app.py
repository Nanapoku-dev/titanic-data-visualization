import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px

# -----------------------------
# LOAD DATA
# -----------------------------
df = pd.read_csv("titanic.csv")

# -----------------------------
# CLEAN DATA
# -----------------------------
df["Age"] = df["Age"].fillna(df["Age"].median())
df["Embarked"] = df["Embarked"].fillna(df["Embarked"].mode()[0])

# -----------------------------
# CREATE DASH APP
# -----------------------------
app = dash.Dash(__name__)

# -----------------------------
# APP LAYOUT
# -----------------------------
app.layout = html.Div([

    # TITLE
    html.H1(
        "Titanic Survival Dashboard",
        style={
            "textAlign": "center",
            "color": "#003366",
            "padding": "20px"
        }
    ),

    # KPI CARDS
    html.Div([

        html.Div([
            html.H3("Total Passengers"),
            html.H2(df.shape[0])
        ], style={
            "backgroundColor": "#D6EAF8",
            "padding": "20px",
            "borderRadius": "10px",
            "width": "30%",
            "textAlign": "center"
        }),

        html.Div([
            html.H3("Total Survivors"),
            html.H2(df["Survived"].sum())
        ], style={
            "backgroundColor": "#D5F5E3",
            "padding": "20px",
            "borderRadius": "10px",
            "width": "30%",
            "textAlign": "center"
        }),

        html.Div([
            html.H3("Average Age"),
            html.H2(round(df["Age"].mean(), 1))
        ], style={
            "backgroundColor": "#FADBD8",
            "padding": "20px",
            "borderRadius": "10px",
            "width": "30%",
            "textAlign": "center"
        })

    ], style={
        "display": "flex",
        "justifyContent": "space-around",
        "marginBottom": "30px"
    }),

    # FILTERS
    html.Div([

        # CLASS FILTER
        html.Div([
            html.Label("Select Passenger Class"),

            dcc.Dropdown(
                id="class-filter",
                options=[
                    {"label": "First Class", "value": 1},
                    {"label": "Second Class", "value": 2},
                    {"label": "Third Class", "value": 3}
                ],
                value=1,
                clearable=False
            )

        ], style={"width": "45%"}),

        # GENDER FILTER
        html.Div([
            html.Label("Select Gender"),

            dcc.Dropdown(
                id="gender-filter",
                options=[
                    {"label": "Male", "value": "male"},
                    {"label": "Female", "value": "female"}
                ],
                value="male",
                clearable=False
            )

        ], style={"width": "45%"})

    ], style={
        "display": "flex",
        "justifyContent": "space-around",
        "marginBottom": "30px"
    }),

    # CHARTS
    dcc.Graph(id="age-chart"),

    dcc.Graph(id="survival-chart"),

    dcc.Graph(id="fare-chart")

], style={
    "padding": "20px",
    "fontFamily": "Arial"
})

# -----------------------------
# CALLBACK FUNCTION
# -----------------------------
@app.callback(
    Output("age-chart", "figure"),
    Output("survival-chart", "figure"),
    Output("fare-chart", "figure"),
    Input("class-filter", "value"),
    Input("gender-filter", "value")
)

def update_dashboard(selected_class, selected_gender):

    filtered_df = df[
        (df["Pclass"] == selected_class) &
        (df["Sex"] == selected_gender)
    ]

    # AGE DISTRIBUTION
    fig1 = px.histogram(
        filtered_df,
        x="Age",
        nbins=20,
        title="Age Distribution"
    )

    # SURVIVAL PIE CHART
    fig2 = px.pie(
        filtered_df,
        names="Survived",
        title="Survival Rate"
    )

    # FARE DISTRIBUTION
    fig3 = px.box(
        filtered_df,
        y="Fare",
        title="Fare Distribution"
    )

    return fig1, fig2, fig3

# -----------------------------
# RUN APP
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)