import pandas as pd
import numpy as np
from sklearn import metrics
from statsmodels.formula.api import ols
from sklearn.model_selection import train_test_split
import mape

class linear:
    def __init__(self, RawData, training_size):
        self.data = RawData
        self.size = training_size
        self.__model
        self.train_data, self.test_data = train_test_split(RawData, train_size = training_size)

    def linear_regression(self):
        regression = ols(formula='Y~.', data = self.train_data)
        lm = regression.fit()
        self.__model = lm
        y_pred = pd.DataFrame(round(lm.predict(self.data), 0), columns=['Predicted_Y'])
        PredictData = y_pred.join(self.data)
        return PredictData

    def result(self):
        y_pred = round(self.__model.predict(self.train_data), 0)
        y_true = self.train_data["Y"]
        training_MAPE =  str(round(mape(y_true, y_pred), 4))+'%'
        y_pred = round(self.__model.predict(self.test_data), 0)
        y_true = self.test_data["Y"]
        testing_MAPE =  str(round(mape(y_true, y_pred), 4))+'%'
        return training_MAPE, testing_MAPE