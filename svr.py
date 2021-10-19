import pandas as pd  
import numpy as np  
from sklearn.svm import SVR
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
import mape

class svr:
    def __init__(self, RawData, training_size):
        self.data = RawData
        self.size = training_size
        self.__model
        train_data, test_data = train_test_split(RawData, train_size = training_size)
        self.train_x = train_data.iloc[:,1:]
        self.train_y = train_data.iloc[:,0]
        self.test_x = test_data.iloc[:,1:]
        self.test_y = test_data.iloc[:,0]

    def support_vector_regression(self):
        param = {'kernel':'rbf', 'C':[*range(0.1, 1, 0.1), *range(1, 30, 1), *range(30, 100, 5)], 'gamma':('auto', 'scale')}
        grids = GridSearchCV(SVR(), param, scoring='r2')#cv cross validation C gamma scoring?
        grids.fit(self.train_x, self.train_y)
        self.__model = grids
        y_pred = pd.DataFrame(round(grids.predict(self.data), 0), columns=['Predicted_Y'])
        PredictData = y_pred.join(self.data)
        return PredictData

    def result(self):
        y_pred = round(self.__model.predict(self.train_x), 0)
        training_MAPE = str(round(mape(self.train_y, y_pred), 4))+'%'
        y_pred = round(self.__model.predict(self.test_x), 0)
        testing_MAPE =  str(round(mape(self.test_y, y_pred), 4))+'%'
        return training_MAPE, testing_MAPE