from dash import Dash, html, dcc, Input, Output, State
from predictive_market_analysis.dashboard.callback_classes import StockDropDown, TimeFrameDropDown, MLModelSelect
from predictive_market_analysis.database.database_config import Database
from predictive_market_analysis.ml_model.model_config import MLModelConfig
from predictive_market_analysis.ml_model.neural_network import LSTMModel
import plotly.express as px
import pandas as pd

class DashBoard():
    def __init__(self, logger, database: Database, model: MLModelConfig):
        self.logger = logger
        self.app = Dash()
        self.x = 'date'
        self.y = 'close'
        self.styles = {
            'background': '#F9F9F9',
            'text': '#333333',
            'font_family': 'Times New Roman'
        }
        self.database = database
        self.model = model
        self.stock = 'aapl'
        self.timeframe = 'daily'
        self.default_data = self.database.select(f'{self.stock}_{self.timeframe}', ['date', 'close'])
        self.stock_symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']
        self.timeframes = ['daily', 'weekly', 'monthly']
        self.machine_learning_models = ['','Long-Short-Term-Memory']

    def layout(self, title: str, subtitle: str = None):
        self.logger.log('Setting up the layout')
        sub = subtitle if subtitle is not None else ''
        try:
            self.fig = px.line(self.default_data, x=self.x, y=self.y)
            self.app.layout = html.Div(children=[
                html.H1(
                    children=title,
                    style={
                            'textAlign': 'center',
                            'color': self.styles['text'],
                            'fontFamily': self.styles['font_family']
                        }
                    ),
                html.Div(
                    children=sub, 
                    style={
                        'textAlign': 'center',
                        'color': self.styles['text']
                        }
                    ),
                html.Div(
                    children=[
                        html.Div([
                            dcc.Dropdown(
                                options=[{'label': stock, 'value': stock} for stock in self.stock_symbols],
                                value=self.stock.upper(),
                                id='stock-dropdown', 
                                style={'width': '200px'}
                            ),
                            dcc.Dropdown(
                                options=[{'label': tf, 'value': tf} for tf in self.timeframes],
                                value=self.timeframe,
                                id='timeframe-dropdown', 
                                style={'width': '200px', 'marginTop': '10px'}
                            )
                        ],
                        style={
                            'display': 'flex',
                            'flexDirection': 'column', 
                            'alignItems': 'center'
                        }),
                        html.Div([
                            dcc.Dropdown(
                                options=[{'label': model, 'value': model} for model in self.machine_learning_models],
                                value=self.machine_learning_models[0],
                                id='ml-model-select',
                                style={'width': '300px'}
                            ),
                            dcc.Input(
                                id='ml-lookback',
                                type='text',
                                placeholder='Enter a lookback period',
                                style={'width': '200px', 'marginTop': '10px'}
                            ),
                            dcc.Input(
                                id='ml-forecast',
                                type='text',
                                placeholder='Enter a forecast period',
                                style={'width': '200px', 'marginTop': '10px'}
                            ),
                            html.Button('Run Forecast Model', id='submit-button', n_clicks=0),
                        ],
                        style={
                            'display': 'flex',
                            'alignItems': 'center',
                            'marginLeft': 'auto',
                            'flexDirection': 'column'
                        })
                    ],
                    style={
                        'display': 'flex',
                        'justifyContent': 'space-between',
                        'width': '80%',
                        'margin': 'auto' 
                    }
                ),
                dcc.Graph(
                    id='price-graph',
                    figure=self.fig
                )
            ])

            self.setup_callbacks()

        except Exception as e:
            self.logger.log(f'Error setting up layout: {e}', 'ERROR')
            raise ValueError(f"Error setting up layout: {e}")

    def handle_callback(self, stock_model, timeframe_model, ml_model):
        try:
            if isinstance(stock_model, StockDropDown) and isinstance(timeframe_model, TimeFrameDropDown):
                self.stock = stock_model.value[0].lower()
                self.timeframe = timeframe_model.value[0]
                self.logger.log(f'Updating graph with stock: {self.stock} and timeframe: {self.timeframe}')
                self.default_data = self.database.select(f'{self.stock}_{self.timeframe}', ['date', 'close'])
            if isinstance(ml_model, MLModelSelect) and not ml_model.no_model:
                if ml_model.model[0] == 'Long-Short-Term-Memory':
                    self.logger.log('Running LSTM model')
                    self.default_data = self.model.forecast(LSTMModel(self.default_data, ml_model.lookback, ml_model.forecast))
        except Exception as e:
            raise ValueError(f"Invalid callback model: {e}")

        self.fig = px.line(self.default_data, x=self.x, y=self.y)

    def setup_callbacks(self):
        @self.app.callback(
            Output('price-graph', 'figure'),
            [Input('stock-dropdown', 'value'),
            Input('timeframe-dropdown', 'value'),
            Input('ml-model-select', 'value'),
            State('ml-lookback', 'value'),
            State('ml-forecast', 'value'),
            Input('submit-button', 'n_clicks')]
        )
        def update_graph(stock_dropdown, timeframe_dropdown, ml_model, ml_lookback, ml_forecast, n_clicks):
            ml_params = {}
            if n_clicks > 0:
                ml_params = {
                    'model': ml_model,
                    'lookback': ml_lookback,
                    'forecast': ml_forecast
                }
            stock = stock_dropdown if stock_dropdown else self.stock
            timeframe = timeframe_dropdown if timeframe_dropdown else self.timeframe
            self.handle_callback(StockDropDown(stock), TimeFrameDropDown(timeframe), MLModelSelect(ml_params))
            return self.fig
    def run(self):
        self.app.run_server(debug=True)