from dash import html, dcc, Output, Input, Dash
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from dash_iconify import DashIconify
import glob
import pandas as pd
import random

df = pd.read_csv('static/EVIndia.csv')
df.fillna('Not Available')


def drop_items(menu, item_list, wid=1):
    return dbc.Col(dbc.DropdownMenu([dbc.DropdownMenuItem(
        item, n_clicks=0,

    ) for item in item_list], label=menu, color='white', direction='down', className="d-flex justify-content-center",
    ),
        width=wid, align='center')


def sub_nav_bar():
    return dbc.Row([drop_items("Electronics", ['Mobile', 'Laptop', 'Desktop Pc'], 1),
                    drop_items("TV's & Appliances",
                               ['Television', 'Washing Machine', 'Kitchen Appliances', "Refrigerators",
                                "Air Conditioners", "Small Home Appliances"], 2),
                    drop_items("Men", ['Footwear', 'Clothing', 'Watches'], wid=1),
                    drop_items("Women", ['Beauty & Grooming', 'Footwear', 'Clothing', 'Watches']),
                    drop_items("Baby & Kids", ['Beauty & Grooming', 'Footwear', 'Clothing', 'Watches']),
                    drop_items("Home & furniture", ['Beauty & Grooming', 'Footwear', 'Clothing', 'Watches'], 2),
                    drop_items("Sports, Books & More", ['Beauty & Grooming', 'Footwear', 'Clothing', 'Watches'], 2),
                    dbc.Col(dcc.Link("Flights", href="#", style={'text-decoration': 'None', 'color': 'black'}),
                            width=1),
                    dbc.Col(dcc.Link("Offer Zone", href="#", style={'text-decoration': 'None', 'color': 'black'}),
                            width=1)
                    ], justify='center')


def acordiation():
    return dbc.Accordion(
        [
            dbc.AccordionItem(
                [
                    html.H5('TATA'),
                    html.H5('Hyundai'),
                    html.H5('MG'),
                    html.H5('Jaguar'),
                    html.H5('Audi'),
                    html.H5('Mercedes Benz'),
                    html.H5('Porsche Taycan'),
                    html.H5('BMW'),
                ],
                title="Brand",
            ),
            dbc.AccordionItem([
                dcc.Checklist([' 50 % or More', ' 40 % or More', ' 30 % or More', ' 20 % or More', ' 10 % or More'],
                              className="d-flex flex-column")], title="Discount"),
            dbc.AccordionItem(
                dcc.Checklist([" Include Out Of Stock"], className="d-flex flex-column"),title="Availability"),
            dbc.AccordionItem(
                "This is the content of the third section",
                title="Primary Material",
            ),
        ],
    )


def sidemenu():
    return [
        dbc.Col(html.H3('Filters'), style={'padding': '5px'}),
        html.Br(),
        dbc.Col(html.H6('PRICE')),
        html.Br(),
        dbc.Col(dcc.RangeSlider(0, 20000000, 1, marks=None, value=[0, 20000000],
                                tooltip={"placement": "bottom", "always_visible": True})),
        html.Br(),
        dbc.Col(acordiation())

    ]


def carosal(path):
    files = glob.glob(path)
    files = [file.replace("\\", "/") if "\\" in file else file for file in files]
    return dbc.Carousel(
        items=[
            {
                "key": "1",
                "src": f"{path}",
                "img_style": {'height': '40vh', 'width': '50vh'}
            } for path in files
        ], interval=random.randint(1000, 2000), ride="carousel",indicators=False,)


def card(data):
    return dbc.Card([dbc.Col(carosal(data['Image_Path'])),
                     dbc.CardBody([
                         html.H3(data['Car']),
                         html.H6(data['Style']),
                         html.H6("Range - " + data['Range']),
                         html.H6('Transmission - ' + data['Transmission']),
                         html.H6('Capacity - ' + data['Capacity']),
                         html.H4(data['PriceRange']),
                         html.P('*Ex showroom price', style={'font-size': '12px'}),
                     ]
                     )], style={'margin': '1px'}, className="shadow-lg",

                    )


final_cards = [
    dbc.Row(dbc.Col(html.H3('Electric Cars In India', style={'text-align': 'center'}), width=12), justify='center')]
cards = []
for i, row in df.iterrows():
    cards.append(dbc.Col(card(row), width=4, style={'padding': '2px'}))
    if len(cards) == 3 or (i + 1) == len(df):
        final_cards.append(dbc.Row(cards, justify='center', style={'margin': '5px'}))
        cards = []

    # print(cards)

app = Dash(external_stylesheets=[dbc.themes.COSMO])
app.layout = dbc.Container(
    [dbc.Row([dbc.Row(dbc.Col(dbc.Row([dbc.Col(html.H4("FlapKart", style={'color': 'yellow', "font-weight": "bold",
                                                                          "font-style": "italic"}), width=2),
                                       dbc.Col(dcc.Input(placeholder="Search", className="form-control me-sm-2"),
                                               width=4),
                                       dbc.Col(html.Button('logIn'), width=1),
                                       dbc.Col(html.H6('Become a seller',
                                                       style={'text-decoration': 'None', 'color': 'white',
                                                              'margin-top': '5px'},
                                                       className="d-flex justify-content-center"), width=2),
                                       dbc.Col(dbc.DropdownMenu([dbc.DropdownMenuItem(
                                           "A button", n_clicks=0
                                       ), dbc.DropdownMenuItem(
                                           "A button", n_clicks=0
                                       )], label="More"), width=1),
                                       dbc.Col(
                                           [html.Span(['Cart ', DashIconify(icon="noto-v1:shopping-cart", width=40)],
                                                      style={'color': 'white'})],
                                           width=2)]), width=8),
                      className="navbar navbar-expand-lg navbar-dark bg-primary", justify='center'),
              dbc.Row(dbc.Col(sub_nav_bar(), width=10), className="navbar navbar-expand-lg navbar-light bg-light",
                      justify='center')], style={"position": "sticky", "top": 0, 'z-index': '100'}),
     dbc.Row(
         [dbc.Col(dbc.Row(dbc.Col(sidemenu(), style={'padding': '1px'}, className="shadow-lg"),
                          style={"position": "sticky", "top": 0, 'z-index': 100}), width=2),
          dbc.Col(dbc.Row(dbc.Col(final_cards, width=12, className="shadow-lg", style={'padding': '1px'}),
                          style={'margin-left': '5px', 'overflow-y': 'scroll', 'max-height': '90vh',
                                 'overflow-x': 'hidden'}), width=10)],
         style={'margin': '5px'})],
    fluid=True,
    style={'padding': '0', 'margin': '0'})
if __name__ == '__main__':
    app.run_server(debug=True)
