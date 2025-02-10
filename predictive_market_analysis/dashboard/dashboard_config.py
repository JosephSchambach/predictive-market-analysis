from dash import Dash, html, dcc, Input, Output
from predictive_market_analysis.dashboard.callback_classes import StockDropDown, TimeFrameDropDown, MLModelSelect
from predictive_market_analysis.database.database_config import Database
import plotly.express as px
import pandas as pd

class DashBoard():
    def __init__(self, logger, database: Database):
        self.logger = logger
        self.app = Dash()
        self.x = 'date'
        self.y = 'close'
        self.colors = {
            'background': '#F9F9F9',
            'text': '#333333',
            'font_family': 'Times New Roman'
        }
        self.database = database
        self.stock = 'aapl'
        self.timeframe = 'daily'
        self.default_data = self.database.select(f'{self.stock}_{self.timeframe}', ['date', 'close'])

    def layout(self, title: str, subtitle: str = None):
        self.logger.log('Setting up the layout')
        sub = subtitle if subtitle is not None else ''
        try:
            self.fig = px.line(self.default_data, x=self.x, y=self.y)
            self.app.layout = html.Div(children=[
                html.H1(children=title,
                        style={
                        'textAlign': 'center',
                        'color': self.dashboard_config['text']
                        'fontFamily': self.dashboard_config['font_family']
                    }),
                html.Div(children=sub, 
                        style={
                    'textAlign': 'center',
                    'color': self.colors['text']}),
                html.Div(children=[
                    dcc.Dropdown(
                        options=['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA'],
                        value=self.stock.upper(),
                        id='stock-dropdown', 
                    ),
                    dcc.Dropdown(
                        id='timeframe-dropdown', 
                        value=self.timeframe,
                        options=['daily', 'weekly', 'monthly'],
                    )
                ]),
                dcc.Graph(
                    id='price-graph',
                    figure=self.fig
                )
            ])

            self.setup_callbacks()

        except Exception as e:
            self.logger.log(f'Error setting up layout: {e}', 'ERROR')
            raise ValueError(f"Error setting up layout: {e}")

    def handle_callback(self,callback_model):
        if isinstance(callback_model, StockDropDown):
            self.stock = callback_model.value[0].lower()
        elif isinstance(callback_model, TimeFrameDropDown):
            self.timeframe = callback_model.value[0]
        elif isinstance(callback_model, MLModelSelect):
            pass
        else:
            raise ValueError('Invalid callback model')

        self.logger.log(f'Updating graph with stock: {self.stock} and timeframe: {self.timeframe}')
        self.default_data = self.database.select(f'{self.stock}_{self.timeframe}', ['date', 'close'])

        self.fig = px.line(self.default_data, x=self.x, y=self.y)

    def setup_callbacks(self):
        @self.app.callback(
            Output('price-graph', 'figure'),
            [Input('stock-dropdown', 'value'),
            Input('timeframe-dropdown', 'value')]
        )
        def update_graph(stock_dropdown, timeframe_dropdown):
            stock = stock_dropdown if stock_dropdown else self.stock
            timeframe = timeframe_dropdown if timeframe_dropdown else self.timeframe
            self.handle_callback(StockDropDown(stock))
            self.handle_callback(TimeFrameDropDown(timeframe))

            return self.fig
    def run(self):
        self.app.run_server(debug=True)