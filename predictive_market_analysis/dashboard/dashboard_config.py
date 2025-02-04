from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

class DashBoard():
    def __init__(self, logger):
        self.logger = logger
        self.app = Dash()
        self.colors = {
            'background': '#F9F9F9',
            'text': '#333333'
        }

    def layout(self, title: str, x: str, y: str, data: pd.DataFrame, subtitle: str = None):
        self.logger.log('Setting up the layout')
        sub = subtitle if subtitle is not None else ''
        try:
            self.fig = px.line(data, x=x, y=y)
            self.app.layout = html.Div(children=[
                html.H1(children=title,
                        style={
                        'textAlign': 'center',
                        'color': self.colors['text']
                    }),
                html.Div(children=sub, 
                        style={
                    'textAlign': 'center',
                    'color': self.colors['text']}),
                dcc.Graph(
                    id='price-graph',
                    figure=self.fig
                )
            ])
        except Exception as e:
            self.logger.log(f'Error setting up layout: {e}', 'ERROR')
            raise ValueError(f"Error setting up layout: {e}")

    def run(self):
        self.app.run_server(debug=True)