import dash
from dash import html, dcc
from dash.dependencies import Input, Output

import pandas as pd
import numpy as np

import plotly.graph_objs as go
import plotly.express as px


app = dash.Dash(__name__)
server = app.server

# ========== Data Preparation ========== #
df_data = pd.read_csv("./data/supermarket_sales.csv")
df_data["Date"] = pd.to_datetime(df_data["Date"])

# ========== Layout ========== #
app.layout = html.Div([
    html.H5("Cidades:"),
    dcc.Checklist(df_data["City"].value_counts().index,
                  df_data["City"].value_counts().index, id="check_city"),

    html.H5("Variável de análise:"),
    dcc.RadioItems(["gross income", "Rating"], "gross income", id="main_variable"),

    dcc.Graph(id="city_fig"),
    dcc.Graph(id="pay_fig"),
    dcc.Graph(id="income_per_product_fig"),


])


# ========== Callbacks ========== #
@app.callback([
    Output("city_fig", "figure"),
    Output("pay_fig", "figure"),
    Output("income_per_product_fig", "figure"),
],
[
    Input("check_city", "value"),
    Input("main_variable", "value")
])
def render_graphs(city_list, main_variable):
    operation = np.sum if main_variable == "gross income" else np.mean
    df_filtered = df_data[df_data["City"].isin(city_list)]
    df_city = df_filtered.groupby("City")[main_variable].apply(operation).to_frame().reset_index()
    df_payment = df_filtered.groupby("Payment")[main_variable].apply(operation).to_frame().reset_index()
    df_product = df_filtered.groupby(["Product line","City"])[main_variable].apply(operation).to_frame().reset_index()


    city_fig = px.bar(df_city, x="City", y=main_variable)
    pay_fig = px.bar(df_payment, y="Payment", x=main_variable,orientation="h")
    income_per_product_fig = px.bar(df_product, x="Product line", y="Product line", color="City",orientation="h",barmode="group")

    city_fig.update_layout(margin=dict(l=0, r=0, t=20, b=0),height=200)
    pay_fig.update_layout(margin=dict(l=0, r=0, t=20, b=0),height=200)
    income_per_product_fig.update_layout(margin=dict(l=0, r=0, t=20, b=0),height=500)


    return city_fig,pay_fig,income_per_product_fig

# ========== Run Server ========== #
if __name__ == '__main__':
    app.run_server(port = 8050, debug = True)
