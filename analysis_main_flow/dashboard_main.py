from predictive_market_analysis.context import MarketPredictorContext
from predictive_market_analysis.dashboard import dashboard_config
from dash import callback, Input, Output
from predictive_market_analysis.dashboard.callback_classes import StockDropDown, TimeFrameDropDown, MLModelSelect

context = MarketPredictorContext()

context.dashboard.layout(title='Stock Price', x='date', y='close', data=context.database.select('apple_data_raw', ['date', 'close']))
context.dashboard.run()


@callback(
    Output('price_graph', 'figure'),
    Input('stock-dropdown', 'value')
)
def update_graph_stock_dropdown(stock_dropdown):
    fig = context.dashboard.handle_callback(StockDropDown(stock_dropdown))
    return fig