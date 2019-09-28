'''
Dash plot to showcase vertical alignment of various graph chart
date 27-08-19
'''
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd
#import numpy as np
import sqlalchemy
import pymysql
import datetime
from pandas_datareader import data as pdata


from components import plot_scatter, plot_vol,plot_technical,get_markdown

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', dbc.themes.BOOTSTRAP, dbc.themes.GRID, dbc.themes.CERULEAN]

dash_app = dash.Dash(name = __name__, external_stylesheets=external_stylesheets)
app  =dash_app.server

dash_app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>Nifty Easy Hain | PE Ratio, PB Ratio & Dividend Yield Chart | Nifty Sector Chart</title>
        {%favicon%}
        {%css%}
    </head>
    <body>
        <div></div>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
        <div></div>
    </body>
</html>
'''

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color': 'white',
    'padding': '6px'
}


dash_app.config['suppress_callback_exceptions'] = True

#initialize MYSQL connection to fetch data
engine = sqlalchemy.create_engine('mysql+pymysql://xdenachw:1k)72C2ojaMR(Z@104.37.86.29:3306/xdenachw')

#extract nifty100 stocks trading close price in df
data = pd.read_sql_query("select IndexName,IndexDate,ClosingIndexValue,PE,PB,DivYield,Volume from nse_indclose", engine)

data['IndexDate']= pd.to_datetime(data['IndexDate'])
data.set_index('IndexDate',inplace =True)
data.sort_index(inplace =True)

#extract nifty100 stocks trading close price in df
nifty100 = pd.read_sql_query("select ni.symbol,ni.company_name,ni.industry from nse_indices ni WHERE ni.series ='EQ' and ni.indices ='nifty100'", engine)
#disponse connection engine
engine.dispose()

dropdict =nifty100[['company_name','symbol']]
dropdict.rename(columns={"company_name": "label", "symbol": "value"},inplace= True)
dropdict['value'] = dropdict['value'].astype(str) + '.NS'

dropdown = dcc.Dropdown(
    id='dropdown',
    options=dropdict.to_dict('record'),
    value = 'ABB.NS'
)

#app.scripts.config.serve_locally = False

checklist = dbc.FormGroup(
    [
        dbc.Checklist(
            options=[
                {'label': 'Volume', 'value': 'Volume'},
                {'label': 'Bollinger Bands', 'value': 'Bollinger'},
                {'label': 'Stochastic Oscillator', 'value': 'Stoch'},
                {'label': 'Relative Strength Index', 'value': 'RSI'}
            ],
            inline=True,
            style={'color':'blue'},
            value=['Volume'],
            id='checklist-input',
        ),
    ]
)

textareas = html.Div([
    html.P(id ='textid'),
])


graph = dcc.Graph(
    id='homegraph'
)

heading = html.Div(children=[
    html.H4(dcc.Markdown('''
                    Welcome to **Nifty 100** stock technical indicator dashboard. Technical analysis is an analysis methodology for forecasting the direction of prices through the study of past market data, primarily price and volume. [Check technical indicator details](https://en.wikipedia.org/wiki/Technical_analysis)
                    This dashboard contains 3 key technical indicator viz **Bollinger bands** – a range of price volatility **Relative strength index (RSI)** – oscillator showing price strength and **Stochastic oscillator** – close position within recent trading range.
                '''
            )
    ),
    html.H5(children=['Choose Stock Name from the below list & technical indicator for details'])
])


vertical = False

if not vertical:
    dash_app.layout = html.Div([
        # Page Header
        html.Div([ 
            html.H2(dcc.Markdown(get_markdown('banner'))),
        ],className="banner"),
        html.A([
            html.Img(
                src='https://cdn4.iconfinder.com/data/icons/currency-rupee-4/40/Rupee_hand_money_coin_cash-512.png',
                )
        ], href='https://rzp.io/l/ExpeiCt', target='_blank',className="banner"),
        #Main body
        html.Div([
        html.Div([
            dcc.Tabs(
                children=[
                    dcc.Tab(label = 'Home',value = '0',selected_style=tab_selected_style,children=[
                        html.Div([heading,dropdown, checklist,textareas, graph
                        ])
                    ]),
                    dcc.Tab(label = 'Broad Market', value = '1',selected_style=tab_selected_style,children=[
                        html.Div([
                            dcc.Tabs(
                                    className="tab_style",
                                    children=[
                                    dcc.Tab(label = 'Nifty 50', value = '1', selected_style=tab_selected_style),
                                    dcc.Tab(label = 'Nifty Next 50',value = '2', selected_style=tab_selected_style),
                                    dcc.Tab(label = 'Nifty 100',value = '3', selected_style=tab_selected_style),
                                    dcc.Tab(label = 'Nifty 200',value = '4', selected_style=tab_selected_style),
                                    dcc.Tab(label = 'Nifty Midcap 50',value = '5', selected_style=tab_selected_style),
                                    dcc.Tab(label = 'Nifty Midcap 100',value = '6', selected_style=tab_selected_style),
                                    dcc.Tab(label = 'Nifty Smallcap 100',value = '7', selected_style=tab_selected_style),
                                ],
                                value='1',
                                id='tabs1',
                                vertical=False
                            ),
                        ])
                    ]),
                    dcc.Tab(label = 'Sector',value = '2',selected_style=tab_selected_style,children=[
                        html.Div([
                            dcc.Tabs(
                                className="tab_style",
                                children=[
                                    dcc.Tab(label = 'Auto', value = '1', selected_style=tab_selected_style),
                                    dcc.Tab(label = 'Bank',value = '2', selected_style=tab_selected_style),
                                    dcc.Tab(label = 'Fin Service',value = '3', selected_style=tab_selected_style),
                                    dcc.Tab(label = 'FMCG',value = '4', selected_style=tab_selected_style),
                                    dcc.Tab(label = 'IT',value = '5', selected_style=tab_selected_style),
                                    dcc.Tab(label = 'Media',value = '6', selected_style=tab_selected_style),
                                    dcc.Tab(label = 'Metal',value = '7', selected_style=tab_selected_style),
                                    dcc.Tab(label = 'MNC',value = '8', selected_style=tab_selected_style),
                                    dcc.Tab(label = 'Pharma',value = '9', selected_style=tab_selected_style),
                                    dcc.Tab(label = 'PSU Bank',value = '10', selected_style=tab_selected_style),
                                    dcc.Tab(label = 'Realty',value = '11', selected_style=tab_selected_style),
                                ],
                                value='1',
                                id='tabs2',
                                vertical=False
                            ),
                        ])
                    ]),
                    dcc.Tab(label = 'Thematic',value = '3',selected_style=tab_selected_style),
                    dcc.Tab(label = 'Miscellaneous',value = '4',selected_style=tab_selected_style),
                    dcc.Tab(label = 'Contact Us',value = '5',selected_style=tab_selected_style,children=[
                        html.H4(dcc.Markdown(get_markdown('Contact Us'))),
                        html.A([
                            html.H1('Email Us')
                        ],href='mailto: bitesofjoy03@gmail.com')
                    ]),
                ],
                value='0',
                id='tabs',
                vertical=vertical
            ),
        html.Div(id ='tab-output1'),
        html.Div(
            html.Div(id='tab-output'),
            style={'width': '100%', 'float': 'right'}
        )
        ]),
    ], className ="main_tabs_style")
    ])

else:
    app.layout = html.Div([
        html.Div(
            dcc.Tabs(
            children=[
                dcc.Tab(label = 'Market Value', value = '1'),
                dcc.Tab(label = 'Usage Over Time',value = '2'),
                dcc.Tab(label = 'Predictions',value = '3'),
                dcc.Tab(label = 'Target Pricing',value = '4'),
            ],
            value='3',
            id='tabs',
            vertical=vertical,
                style={
                    'height': '100vh',
                    'borderRight': 'thin lightgrey solid',
                    'textAlign': 'left'
                }
            ),
            style={'width': '20%', 'float': 'left'}
        ),
        html.Div(
            html.Div(id='tab-output'),
            style={'width': '80%', 'float': 'right'}
        )
    ], style={
        'fontFamily': 'Sans-Serif',
        'margin-left': 'auto',
        'margin-right': 'auto',
    })


@dash_app.callback(Output('tab-output', 'children'), 
              [Input('tabs1', 'value'),
               Input('tabs2', 'value'),
               Input('tabs', 'value')
              ])
def render_content(tabs1_value,tabs2_value, outer_value):
    if outer_value =='1':
        if tabs1_value == '1':
            return html.Div([
                html.Img(src="https://www.niftyindices.com/images/default-source/new-logo/broad-indices/nifty_50.png",className="image_style"),
                html.H4(dcc.Markdown(get_markdown('Nifty 50-graph'))),
                dcc.Tabs(
                    id='my-dropdown',
                    value='Nifty 50'
                ),
                html.Div([
                    dcc.RadioItems(
                        id="select-freq", value='D', labelStyle={'display': 'inline-block', 'padding': 10},
                        options=[
                            {'label': "Daily", 'value': 'D'}, 
                            {'label': "Weekly", 'value': 'W'}, 
                            {'label': "Monthly", 'value': 'M'},
                            {'label': "Quarterly", 'value': 'Q'},
                        ], 
                    )
                ],style={'textAlign': "center", }),
                dcc.Graph(id='graph'),
                html.H4(dcc.Markdown(get_markdown('Nifty 50-graph1'))),
                dcc.Graph(id='graph1'),
                html.H4(dcc.Markdown(get_markdown('Volume'))),
                dcc.Graph(id='graph2')
            ])      
        elif tabs1_value == '2':
            return html.Div([
                html.Img(src="https://www.niftyindices.com/images/default-source/new-logo/broad-indices/nifty_-next50.png",className="image_style"),
                html.H4(dcc.Markdown(get_markdown('Nifty Next 50-graph'))),
                dcc.Tabs(
                    id='my-dropdown',
                    value='Nifty Next 50'
                ),
                html.Div([
                    dcc.RadioItems(
                        id="select-freq", value='D', labelStyle={'display': 'inline-block', 'padding': 10},
                        options=[
                            {'label': "Daily", 'value': 'D'}, 
                            {'label': "Weekly", 'value': 'W'}, 
                            {'label': "Monthly", 'value': 'M'},
                            {'label': "Quarterly", 'value': 'Q'},
                        ], 
                    )
                ],style={'textAlign': "center", }),
                dcc.Graph(id='graph'),
                html.H4(dcc.Markdown(get_markdown('Nifty Next50-graph1'))),
                dcc.Graph(id='graph1'),
                html.H4(dcc.Markdown(get_markdown('Volume'))),
                dcc.Graph(id='graph2')
            ])
        elif tabs1_value == '3':
            return html.Div([
                html.Img(src="https://www.niftyindices.com/images/default-source/new-logo/broad-indices/nifty_100.png",className="image_style"),
                html.H4(dcc.Markdown(get_markdown('Nifty 100-graph'))),
                dcc.Tabs(
                    id='my-dropdown',
                    value='Nifty 100'
                ),
                html.Div([
                    dcc.RadioItems(
                        id="select-freq", value='D', labelStyle={'display': 'inline-block', 'padding': 10},
                        options=[
                            {'label': "Daily", 'value': 'D'}, 
                            {'label': "Weekly", 'value': 'W'}, 
                            {'label': "Monthly", 'value': 'M'},
                            {'label': "Quarterly", 'value': 'Q'},
                        ], 
                    )
                ],style={'textAlign': "center", }),
                dcc.Graph(id='graph'),
                html.H4(dcc.Markdown(get_markdown('Nifty 100-graph1'))),
                dcc.Graph(id='graph1'),
                html.H4(dcc.Markdown(get_markdown('Volume'))),
                dcc.Graph(id='graph2')
            ])
        elif tabs1_value == '4':
            return html.Div([
                html.Img(src="https://www.niftyindices.com/images/default-source/new-logo/broad-indices/nifty_200.png",className="image_style"),
                html.H4(dcc.Markdown(get_markdown('Nifty 200-graph'))),
                dcc.Tabs(
                    id='my-dropdown',
                    value='Nifty 200'
                ),
                html.Div([
                    dcc.RadioItems(
                        id="select-freq", value='D', labelStyle={'display': 'inline-block', 'padding': 10},
                        options=[
                            {'label': "Daily", 'value': 'D'}, 
                            {'label': "Weekly", 'value': 'W'}, 
                            {'label': "Monthly", 'value': 'M'},
                            {'label': "Quarterly", 'value': 'Q'},
                        ], 
                    )
                ],style={'textAlign': "center", }),
                dcc.Graph(id='graph'),
                html.H4(dcc.Markdown(get_markdown('Nifty 200-graph1'))),
                dcc.Graph(id='graph1'),
                html.H4(dcc.Markdown(get_markdown('Volume'))),
                dcc.Graph(id='graph2')
            ])
        elif tabs1_value == '5':
            return html.Div([
                html.Img(src="https://www.niftyindices.com/images/default-source/new-logo/broad-indices/nifty_midcap50.png",className="image_style"),
                html.H4(dcc.Markdown(get_markdown('Nifty Midcap 50-graph'))),
                dcc.Tabs(
                    id='my-dropdown',
                    value='Nifty Midcap 50'
                ),
                html.Div([
                    dcc.RadioItems(
                        id="select-freq", value='D', labelStyle={'display': 'inline-block', 'padding': 10},
                        options=[
                            {'label': "Daily", 'value': 'D'}, 
                            {'label': "Weekly", 'value': 'W'}, 
                            {'label': "Monthly", 'value': 'M'},
                            {'label': "Quarterly", 'value': 'Q'},
                        ], 
                    )
                ],style={'textAlign': "center", }),
                dcc.Graph(id='graph'),
                html.H4(dcc.Markdown(get_markdown('Nifty Midcap 50-graph1'))),
                dcc.Graph(id='graph1'),
                html.H4(dcc.Markdown(get_markdown('Volume'))),
                dcc.Graph(id='graph2')
            ])
        elif tabs1_value == '6':
            return html.Div([
                html.Img(src="https://www.niftyindices.com/images/default-source/new-logo/broad-indices/nifty_midcap100.png",className="image_style"),
                html.H4(dcc.Markdown(get_markdown('NIFTY Midcap 100-graph'))),
                dcc.Tabs(
                    id='my-dropdown',
                    value='NIFTY Midcap 100'
                ),
                html.Div([
                    dcc.RadioItems(
                        id="select-freq", value='D', labelStyle={'display': 'inline-block', 'padding': 10},
                        options=[
                            {'label': "Daily", 'value': 'D'}, 
                            {'label': "Weekly", 'value': 'W'}, 
                            {'label': "Monthly", 'value': 'M'},
                            {'label': "Quarterly", 'value': 'Q'},
                        ], 
                    )
                ],style={'textAlign': "center", }),
                dcc.Graph(id='graph'),
                html.H4(dcc.Markdown(get_markdown('NIFTY Midcap 100-graph1'))),
                dcc.Graph(id='graph1'),
                html.H4(dcc.Markdown(get_markdown('Volume'))),
                dcc.Graph(id='graph2')
            ])
        elif tabs1_value == '7':
            return html.Div([
                html.Img(src="https://www.niftyindices.com/images/default-source/new-logo/broad-indices/nifty_smallcap100.png",className="image_style"),
                html.H4(dcc.Markdown(get_markdown('NIFTY Smallcap 100-graph'))),
                dcc.Tabs(
                    id='my-dropdown',
                    value='NIFTY Smallcap 100'
                ),
                html.Div([
                    dcc.RadioItems(
                        id="select-freq", value='D', labelStyle={'display': 'inline-block', 'padding': 10},
                        options=[
                            {'label': "Daily", 'value': 'D'}, 
                            {'label': "Weekly", 'value': 'W'}, 
                            {'label': "Monthly", 'value': 'M'},
                            {'label': "Quarterly", 'value': 'Q'},
                        ], 
                    )
                ],style={'textAlign': "center", }),
                dcc.Graph(id='graph'),
                html.H4(dcc.Markdown(get_markdown('NIFTY Smallcap 100-graph1'))),
                dcc.Graph(id='graph1'),
                html.H4(dcc.Markdown(get_markdown('Volume'))),
                dcc.Graph(id='graph2')
            ])
    elif outer_value == '2':
        if tabs2_value == '1':
            return html.Div([
                html.Img(src="https://www.niftyindices.com/images/default-source/new-logo/sectoral-indices/nifty-auto.png",className="image_style"),
                html.H4(dcc.Markdown(get_markdown('Nifty Auto-graph'))),
                dcc.Tabs(
                    id='my-dropdown',
                    value='Nifty Auto'
                ),
                html.Div([
                    dcc.RadioItems(
                        id="select-freq", value='D', labelStyle={'display': 'inline-block', 'padding': 10},
                        options=[
                            {'label': "Daily", 'value': 'D'}, 
                            {'label': "Weekly", 'value': 'W'}, 
                            {'label': "Monthly", 'value': 'M'},
                            {'label': "Quarterly", 'value': 'Q'},
                        ], 
                    )
                ],style={'textAlign': "center", }),
                dcc.Graph(id='graph'),
                html.H4(dcc.Markdown(get_markdown('Nifty Auto-graph1'))),
                dcc.Graph(id='graph1'),
                html.H4(dcc.Markdown(get_markdown('Volume'))),
                dcc.Graph(id='graph2')
            ])      
        elif tabs2_value == '2':
            return html.Div([
                html.Img(src="https://www.niftyindices.com/images/default-source/new-logo/sectoral-indices/nifty-bank.png",className="image_style"),
                html.H4(dcc.Markdown(get_markdown('Nifty Bank-graph'))),
                html.Div([
                    dcc.RadioItems(
                        id="select-freq", value='D', labelStyle={'display': 'inline-block', 'padding': 10},
                        options=[
                            {'label': "Daily", 'value': 'D'}, 
                            {'label': "Weekly", 'value': 'W'}, 
                            {'label': "Monthly", 'value': 'M'},
                            {'label': "Quarterly", 'value': 'Q'},
                        ], 
                    )
                ],style={'textAlign': "center", }),
                dcc.Tabs(
                    id='my-dropdown',
                    value='Nifty Bank'
                ),
                dcc.Graph(id='graph'),
                html.H4(dcc.Markdown(get_markdown('Nifty Bank-graph1'))),
                dcc.Graph(id='graph1'),
                html.H4(dcc.Markdown(get_markdown('Volume'))),
                dcc.Graph(id='graph2')
            ])
        elif tabs2_value == '3':
            return html.Div([
                html.Img(src="https://www.niftyindices.com/images/default-source/new-logo/sectoral-indices/nifty-financial-services.png",className="image_style"),
                html.H4(dcc.Markdown(get_markdown('Nifty Financial Services-graph'))),
                html.Div([
                    dcc.RadioItems(
                        id="select-freq", value='D', labelStyle={'display': 'inline-block', 'padding': 10},
                        options=[
                            {'label': "Daily", 'value': 'D'}, 
                            {'label': "Weekly", 'value': 'W'}, 
                            {'label': "Monthly", 'value': 'M'},
                            {'label': "Quarterly", 'value': 'Q'},
                        ], 
                    )
                ],style={'textAlign': "center", }),
                dcc.Tabs(
                    id='my-dropdown',
                    value='Nifty Financial Services'
                ),
                dcc.Graph(id='graph'),
                html.H4(dcc.Markdown(get_markdown('Nifty Financial Services-graph1'))),
                dcc.Graph(id='graph1'),
                html.H4(dcc.Markdown(get_markdown('Volume'))),
                dcc.Graph(id='graph2')
            ])
        elif tabs2_value == '4':
            return html.Div([
                html.Img(src="https://www.niftyindices.com/images/default-source/new-logo/sectoral-indices/nifty-fmcg.png",className="image_style"),
                html.H4(dcc.Markdown(get_markdown('Nifty FMCG-graph'))),
                dcc.Tabs(
                    id='my-dropdown',
                    value='Nifty FMCG'
                ),
                html.Div([
                    dcc.RadioItems(
                        id="select-freq", value='D', labelStyle={'display': 'inline-block', 'padding': 10},
                        options=[
                            {'label': "Daily", 'value': 'D'}, 
                            {'label': "Weekly", 'value': 'W'}, 
                            {'label': "Monthly", 'value': 'M'},
                            {'label': "Quarterly", 'value': 'Q'},
                        ], 
                    )
                ],style={'textAlign': "center", }),
                dcc.Graph(id='graph'),
                html.H4(dcc.Markdown(get_markdown('Nifty FMCG-graph1'))),
                dcc.Graph(id='graph1'),
                html.H4(dcc.Markdown(get_markdown('Volume'))),
                dcc.Graph(id='graph2')
            ],)
        elif tabs2_value == '5':
            return html.Div([
                html.Img(src="https://www.niftyindices.com/images/default-source/new-logo/sectoral-indices/nifty-it.png",className="image_style"),
                html.H4(dcc.Markdown(get_markdown('Nifty IT-graph'))),
                dcc.Tabs(
                    id='my-dropdown',
                    value='Nifty IT'
                ),
                html.Div([
                    dcc.RadioItems(
                        id="select-freq", value='D', labelStyle={'display': 'inline-block', 'padding': 10},
                        options=[
                            {'label': "Daily", 'value': 'D'}, 
                            {'label': "Weekly", 'value': 'W'}, 
                            {'label': "Monthly", 'value': 'M'},
                            {'label': "Quarterly", 'value': 'Q'},
                        ], 
                    )
                ],style={'textAlign': "center", }),
                dcc.Graph(id='graph'),
                html.H4(dcc.Markdown(get_markdown('Nifty IT-graph1'))),
                dcc.Graph(id='graph1'),
                html.H4(dcc.Markdown(get_markdown('Volume'))),
                dcc.Graph(id='graph2')
            ])
        elif tabs2_value == '6':
            return html.Div([
                html.Img(src="https://www.niftyindices.com/images/default-source/new-logo/sectoral-indices/nifty-media.png",className="image_style"),
                html.H4(dcc.Markdown(get_markdown('Nifty Media-graph'))),
                dcc.Tabs(
                    id='my-dropdown',
                    value='Nifty Media'
                ),
                html.Div([
                    dcc.RadioItems(
                        id="select-freq", value='D', labelStyle={'display': 'inline-block', 'padding': 10},
                        options=[
                            {'label': "Daily", 'value': 'D'}, 
                            {'label': "Weekly", 'value': 'W'}, 
                            {'label': "Monthly", 'value': 'M'},
                            {'label': "Quarterly", 'value': 'Q'},
                        ], 
                    )
                ],style={'textAlign': "center", }),
                dcc.Graph(id='graph'),
                html.H4(dcc.Markdown(get_markdown('Nifty Media-graph1'))),
                dcc.Graph(id='graph1'),
                html.H4(dcc.Markdown(get_markdown('Volume'))),
                dcc.Graph(id='graph2')
            ])
        elif tabs2_value == '7':
            return html.Div([
                html.Img(src="https://www.niftyindices.com/images/default-source/new-logo/sectoral-indices/nifty-metal.png",className="image_style"),
                html.H4(dcc.Markdown(get_markdown('Nifty Metal-graph'))),
                dcc.Tabs(
                    id='my-dropdown',
                    value='Nifty Metal'
                ),
                html.Div([
                    dcc.RadioItems(
                        id="select-freq", value='D', labelStyle={'display': 'inline-block', 'padding': 10},
                        options=[
                            {'label': "Daily", 'value': 'D'}, 
                            {'label': "Weekly", 'value': 'W'}, 
                            {'label': "Monthly", 'value': 'M'},
                            {'label': "Quarterly", 'value': 'Q'},
                        ], 
                    )
                ],style={'textAlign': "center", }),
                dcc.Graph(id='graph'),
                html.H4(dcc.Markdown(get_markdown('Nifty Metal-graph1'))),
                dcc.Graph(id='graph1'),
                html.H4(dcc.Markdown(get_markdown('Volume'))),
                dcc.Graph(id='graph2')
            ])
        elif tabs2_value == '8':
            return html.Div([
                html.Img(src="https://www.niftyindices.com/images/default-source/new-logo/thematic-indices/nifty__mnc.png",className="image_style"),
                html.H4(dcc.Markdown(get_markdown('Nifty MNC-graph'))),
                dcc.Tabs(
                    id='my-dropdown',
                    value='Nifty MNC'
                ),
                html.Div([
                    dcc.RadioItems(
                        id="select-freq", value='D', labelStyle={'display': 'inline-block', 'padding': 10},
                        options=[
                            {'label': "Daily", 'value': 'D'}, 
                            {'label': "Weekly", 'value': 'W'}, 
                            {'label': "Monthly", 'value': 'M'},
                            {'label': "Quarterly", 'value': 'Q'},
                        ], 
                    )
                ],style={'textAlign': "center", }),
                dcc.Graph(id='graph'),
                html.H4(dcc.Markdown(get_markdown('Nifty MNC-graph1'))),
                dcc.Graph(id='graph1'),
                html.H4(dcc.Markdown(get_markdown('Volume'))),
                dcc.Graph(id='graph2')
            ])
        elif tabs2_value == '9':
            return html.Div([
                html.Img(src="https://www.niftyindices.com/images/default-source/new-logo/sectoral-indices/nifty-pharma.png",className="image_style"),
                html.H4(dcc.Markdown(get_markdown('Nifty Pharma-graph'))),
                dcc.Tabs(
                    id='my-dropdown',
                    value='Nifty Pharma'
                ),
                html.Div([
                    dcc.RadioItems(
                        id="select-freq", value='D', labelStyle={'display': 'inline-block', 'padding': 10},
                        options=[
                            {'label': "Daily", 'value': 'D'}, 
                            {'label': "Weekly", 'value': 'W'}, 
                            {'label': "Monthly", 'value': 'M'},
                            {'label': "Quarterly", 'value': 'Q'},
                        ], 
                    )
                ],style={'textAlign': "center", }),
                dcc.Graph(id='graph'),
                html.H4(dcc.Markdown(get_markdown('Nifty Pharma-graph1'))),
                dcc.Graph(id='graph1'),
                html.H4(dcc.Markdown(get_markdown('Volume'))),
                dcc.Graph(id='graph2')
            ])
        elif tabs2_value == '10':
            return html.Div([
                html.Img(src="https://www.niftyindices.com/images/default-source/new-logo/sectoral-indices/nifty-psu-bank.png",className="image_style"),
                html.H4(dcc.Markdown(get_markdown('Nifty PSU Bank-graph'))),
                dcc.Tabs(
                    id='my-dropdown',
                    value='Nifty PSU Bank'
                ),
                html.Div([
                    dcc.RadioItems(
                        id="select-freq", value='D', labelStyle={'display': 'inline-block', 'padding': 10},
                        options=[
                            {'label': "Daily", 'value': 'D'}, 
                            {'label': "Weekly", 'value': 'W'}, 
                            {'label': "Monthly", 'value': 'M'},
                            {'label': "Quarterly", 'value': 'Q'},
                        ], 
                    )
                ],style={'textAlign': "center", }),
                dcc.Graph(id='graph'),
                html.H4(dcc.Markdown(get_markdown('Nifty PSU Bank-graph1'))),
                dcc.Graph(id='graph1'),
                html.H4(dcc.Markdown(get_markdown('Volume'))),
                dcc.Graph(id='graph2')
            ])
        elif tabs2_value == '11':
            return html.Div([
                html.Img(src="https://www.niftyindices.com/images/default-source/new-logo/sectoral-indices/nifty-realty.png",className="image_style"),
                html.H4(dcc.Markdown(get_markdown('Nifty Realty-graph'))),
                dcc.Tabs(
                    id='my-dropdown',
                    value='Nifty Realty'
                ),
                html.Div([
                    dcc.RadioItems(
                        id="select-freq", value='D', labelStyle={'display': 'inline-block', 'padding': 10},
                        options=[
                            {'label': "Daily", 'value': 'D'}, 
                            {'label': "Weekly", 'value': 'W'}, 
                            {'label': "Monthly", 'value': 'M'},
                            {'label': "Quarterly", 'value': 'Q'},
                        ], 
                    )
                ],style={'textAlign': "center", }),
                dcc.Graph(id='graph'),
                html.H4(dcc.Markdown(get_markdown('Nifty Realty-graph1'))),
                dcc.Graph(id='graph1'),
                html.H4(dcc.Markdown(get_markdown('Volume'))),
                dcc.Graph(id='graph2')
            ])
    elif outer_value == '3':
        return html.Div([
            html.H3('Coming Soon')
        ])
    elif outer_value == '4':
        return html.Div([
            html.H3('Coming Soon')
        ])   

#HOME PAGE callback
@dash_app.callback(Output('homegraph', 'figure'),
             [Input('dropdown', 'value'),
              Input('checklist-input', 'value')])
def update_homegraph(stock, indicators):
    df = pdata.DataReader(stock, 'yahoo', '2018-01-01', str(datetime.datetime.now()).split()[0]).round(1)
    dff = df.reset_index()
    fig = plot_technical(stock,dff,indicators)
    return fig
        
@dash_app.callback(Output('textid', 'children'),
             [Input('dropdown', 'value'),
              Input('checklist-input', 'value')])
def on_form_change(dropdown_value, checklist_value):
    text = ""
    if(checklist_value):
        for val in checklist_value :
            text =''.join([text , get_markdown(val)])
        return html.H4(dcc.Markdown(text))
    else:
        return html.H4(dcc.Markdown(get_markdown(checklist_value)))



@dash_app.callback([
    Output('graph', 'figure'),
    Output('graph1','figure'),
    Output('graph2','figure')
],[Input('my-dropdown', 'value'),
   Input('select-freq', 'value') ])
def update_graph(value,freq):
    IndexName = value
    if freq =='D':
        fig  = plot_scatter(data.loc[data['IndexName'] == IndexName],'ClosingIndexValue')
        fig1 = plot_scatter(data.loc[data['IndexName'] == IndexName],'PE',['PB','DivYield'])
        fig2 = plot_vol(data.loc[data['IndexName'] == IndexName], IndexName )
        return fig,fig1,fig2
    else:
        fig  = plot_scatter(data.loc[data['IndexName'] == IndexName].resample(freq).mean(),'ClosingIndexValue')
        fig1 = plot_scatter(data.loc[data['IndexName'] == IndexName].resample(freq).mean(),'PE',['PB','DivYield'])
        fig2 = plot_vol(data.loc[data['IndexName'] == IndexName].resample(freq).mean(), IndexName )
        return fig,fig1,fig2

if __name__ == '__main__':
    dash_app.run_server(debug=True)
