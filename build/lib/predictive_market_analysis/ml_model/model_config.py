from predictive_ma.ml_model.neural_network import LSTMModel

class MLModelConfig():
    def __init__(self, context): 
        self.context = context
        self.logger = context.logger
    
    def forecast(self, model):
        try:
            self.logger.log('Processing the model')
            model_results = model.run()
            if not model_results.empty:
                self.logger.log(f"Successfully process model results for the model")
                return model_results
            else:
                self.logger.log("Model results are empty", 'ERROR')
                raise ValueError("Model results are empty")
        except Exception as e:
            self.logger.log(f"An error occurred processing the model: {str(e)}", 'ERROR')
            return None
        