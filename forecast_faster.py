import pandas as pd 
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import AdaBoostRegressor
from sklearn import tree
import matplotlib.pyplot as plt

def mape(y_true, y_pred):
    y_true_list = list(y_true)
    y_dif = y_true_list - y_pred
    y_num = len(y_true_list)
    cnt = y_num
    ret = 0
    for i in range(y_num):
        if y_true_list[i] != 0:
            ret += abs(y_dif[i]/y_true_list[i])
        else:
            cnt = cnt-1
    return (ret/cnt)*100

class forecast:
    def __init__(self, RawData, training_size):
        self.data = RawData
        self.size = training_size
        train_data, test_data = train_test_split(RawData, train_size = training_size, random_state=0, shuffle=False)
        self.x_train = train_data.iloc[:,1:]
        self.y_train = train_data.iloc[:,0]
        self.x_test = test_data.iloc[:,1:]
        self.y_test = test_data.iloc[:,0]

    def linear_regression(self):
        self.model = LinearRegression()
        self.model.fit(self.x_train,self.y_train)

    def support_vector_regressor(self):
        '''dif = 1
        best_score = 0
        for gamma in ['auto', 'scale']:
            for c in [*np.arange(0.1, 1, 0.1), *np.arange(1, 30, 1), *np.arange(30, 100, 5), *np.arange(100, 1000, 10)]:
                cls = SVR(gamma=gamma,C=c)
                cls.fit(self.x_train,self.y_train)
                score = cls.score(self.x_test,self.y_test)
                if cls.score(self.x_train, self.y_train)>0 and score>0 and np.abs(cls.score(self.x_train, self.y_train)-score < dif):
                    dif = np.abs(cls.score(self.x_train, self.y_train)-score)
                    best_score = cls.score(self.x_train, self.y_train)
                    test_score = score
                    best_parameters = {'gamma':gamma,"C":c}
                elif cls.score(self.x_train, self.y_train)>best_score:
                    best_score = cls.score(self.x_train, self.y_train)
                    test_score = score
                    best_parameters = {'gamma':gamma,"C":c}
        cls = SVR(**best_parameters)'''
        parameters = {
            'kernel':['rbf'], 
            'C':[*np.arange(0.1, 1, 0.1), *np.arange(1, 30, 1), *np.arange(30, 100, 5), *np.arange(100, 1000, 10)], 
            'gamma':['auto', 'scale']
        }
        model = SVR()
        cls = GridSearchCV(model, parameters, n_jobs=-1)
        cls.fit(self.x_train, self.y_train)
        self.model = cls

    def random_forest_regressor(self):
        '''dif = 1
        best_score = 0
        for n_estimators in range(1,501,50):
            rf = RandomForestRegressor(n_estimators=n_estimators,random_state=0)
            rf.fit(self.x_train,self.y_train)
            score = rf.score(self.x_test,self.y_test)
            if rf.score(self.x_train, self.y_train)>0 and score>0 and np.abs(rf.score(self.x_train, self.y_train)-score < dif):
                dif = np.abs(rf.score(self.x_train, self.y_train)-score)
                best_score = rf.score(self.x_train, self.y_train)
                test_score = score
                best_parameters = {"n_estimators": n_estimators}
            elif rf.score(self.x_train, self.y_train)>best_score:
                best_score = rf.score(self.x_train, self.y_train)
                test_score = score
                best_parameters = {"n_estimators": n_estimators}      
        rf = RandomForestRegressor(**best_parameters)'''
        parameters = {"n_estimators":range(50,451,50)}
        model = RandomForestRegressor()
        gs = GridSearchCV(estimator=model, param_grid=parameters)
        gs.fit(self.x_train, self.y_train)
        self.model = gs

    def Adaboost(self):
        """
        err = 110.0
        best_parameters = []
        for l_type in ['exponential', 'linear', 'square']:
            for depth in range(1, 9):
                for n_est, learn_rate in [(50, 1.0), (100, 0.9), (300, 0.9), (500, 0.9)]:
                    adb = AdaBoostRegressor(base_estimator = tree.DecisionTreeRegressor(max_depth =depth),
                                    n_estimators = n_est,
                                    learning_rate = learn_rate,
                                    loss = l_type,
                                    random_state = 1
                                    )
                    adb.fit(self.x_train, self.y_train)
                    trainy_pred = adb.predict(self.x_train)
                    train_mape = mape(self.y_train, trainy_pred)
                    
                    adb.fit(self.x_test, self.y_test)
                    testy_pred = adb.predict(self.x_test)
                    test_mape = mape(self.y_test, testy_pred) 
                    if abs(train_mape - test_mape) < err:
                        best_parameters = [l_type, depth, n_est, learn_rate]

        self.model = AdaBoostRegressor(base_estimator = tree.DecisionTreeRegressor(max_depth = best_parameters[1]),
                                    n_estimators = best_parameters[2],
                                    learning_rate = best_parameters[3],
                                    loss = best_parameters[0],
                                    random_state = 1
                                    )
        self.model.fit(self.x_train, self.y_train)
        """
        parameters = {
            'base_estimator' : [tree.DecisionTreeRegressor(max_depth = 2), tree.DecisionTreeRegressor(max_depth = 3), tree.DecisionTreeRegressor(max_depth = 4), tree.DecisionTreeRegressor(max_depth = 5), tree.DecisionTreeRegressor(max_depth = 6), tree.DecisionTreeRegressor(max_depth = 7)],
            'n_estimators' : [*np.arange(25, 100, 5)],
            #'n_estimators' : [50,100,150,200,250,500],
            'learning_rate' : [0.0001,0.001,0.01,0.1,0.5,0.75,0.9,1.0],
            'loss' : ['exponential', 'linear', 'square'],
        }
        model = AdaBoostRegressor()
        ada = GridSearchCV(model, parameters, n_jobs=-1)
        ada.fit(self.x_train, self.y_train)
        self.model = ada
        
    def forecast_result(self, NewData, model):
        if(model=='Linear'):
            self.model = self.linear
        elif(model=='SVR'):
            self.model = self.svr
        elif(model=='Random Forest'):
            self.model = self.rmf
        elif(model=='AdaBoost'):
            self.model = self.ada
        y_pred = self.model.predict(NewData)
        y_pred = pd.DataFrame(y_pred, columns=['Predicted_Y'])
        NewData = NewData.reset_index(drop=True)
        PredictData = y_pred.join(NewData)
        return PredictData
        
    def error_result(self, model):
        if(model=='Linear'):
            self.linear_regression()
            self.linear = self.model
        elif(model=='SVR'):
            self.support_vector_regressor()
            self.svr = self.model
        elif(model=='Random Forest'):
            self.random_forest_regressor()
            self.rmf = self.model
        elif(model=='AdaBoost'):  
            self.Adaboost()
            self.ada = self.model
        y_train_pred = self.model.predict(self.x_train)
        training_MAPE = round(mape(self.y_train, y_train_pred), 4)
        y_test_pred = self.model.predict(self.x_test)
        testing_MAPE =  round(mape(self.y_test, y_test_pred), 4)
        return [training_MAPE, testing_MAPE]

class output(forecast):
    def error_chart(self):
        error_list = [self.error_result('Linear'), self.error_result('SVR'), self.error_result('Random Forest'), self.error_result('AdaBoost')]
        df = pd.DataFrame (error_list, columns = ['training', 'testing'], index = ['Linear', 'SVR', 'Random Forest', 'AdaBoost'])
        self.good = []
        for i in error_list:
            if (np.abs(i[1]-i[0])<=5 and i[0]<=15 and i[1]<=15):
                if(error_list.index(i)==0):
                    self.good.append('Linear')
                elif error_list.index(i)==1:
                    self.good.append('SVR')
                elif error_list.index(i)==2:
                    self.good.append('Random Forest')
                else:
                    self.good.append('AdaBoost')
        return df

    def best_model(self):
        error_list = [self.error_result('Linear'), self.error_result('SVR'), self.error_result('Random Forest'), self.error_result('AdaBoost')]
        df = pd.DataFrame (error_list, columns = ['training', 'testing'], index = ['Linear', 'SVR', 'Random Forest', 'AdaBoost'])
        best_mape = 100
        best = 0
        for i in error_list:
            if (np.abs(i[1]-i[0])<=5 and i[0]<=15 and i[1]<=15 and i[1] < best_mape):
                best_mape = i[1]
                best = error_list.index(i)
        return best
    
    def bar_chart(self, df):
        fig = df.plot(kind='bar', stacked=False,
            #color=['r', 'b'],
            rot=0, title='MAPE(%)').get_figure()
        fig.savefig('plot.png')

#if __name__=='__main__':
#    svr()

#example
#data=RDL
#cls = output(RDL, 0.7)
#df = cls.error_chart() return chart of MAPE with each methods
#cls.bar_chart(df) save bar chart png
#cls.good return a list of methods
#cls.forecast_result(Newdata, linear)