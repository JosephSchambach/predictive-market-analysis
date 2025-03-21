from predictive_ma.ml_model.neural_network import LSTMModel

class MLModelConfig():
    def __init__(self, context): 
        self.context = context
        self.logger = context.logger
    
    def forecast(self, model):
        try:
            model_type = type(model).__name__
            self.logger.log(f'Processing the {model_type} model')
            model_results = model.run()
            if not model_results.empty:
                self.logger.log(f"Successfully processed {model_type} results")
                return model_results
            else:
                self.logger.log(f"{model_type} results are empty", 'ERROR')
                raise ValueError("Model results are empty")
        except Exception as e:
            self.logger.log(f"An error occurred processing the {model_type} model: {str(e)}", 'ERROR')
            return None
        