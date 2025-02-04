from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
from predictive_market_analysis.context.predictor_context import MarketPredictorContext

context = MarketPredictorContext()

app = Dash()
colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

data = context.database.select('apple_data_raw', ['date', 'close'])

fig = px.line(data, x='date', y='close')
fig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)

app.layout = html.Div(children=[
    html.H1(children='Predictive Market Analysis',
            style={
            'textAlign': 'center',
            'color': colors['text']
        }),
    html.Div(children='''Apple stock price data.''', 
             style={
        'textAlign': 'center',
        'color': colors['text']}),
    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)