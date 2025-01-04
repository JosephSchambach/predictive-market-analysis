import matplotlib.pyplot as plt
import pandas as pd

class DashboardAPI:
    def __init__(self, logger):
        self.logger = logger

    def plot(self, data: pd.DataFrame, x: str | list, y: str | list, title='plot',xlabel='x', ylabel='y'):
        if isinstance(x, str):
            x = [x]
        if isinstance(y, str):
            y = [y]
        for i in range(len(y)):
            plt.plot(data[x[i]], data[y[i]], label=y[i])
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.yticks([i for i in range(0, round(data[y[0]].max() + 100, -2), 100)])
        plt.legend()
        plt.show()