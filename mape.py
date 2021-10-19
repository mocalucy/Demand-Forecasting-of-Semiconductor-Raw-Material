import numpy as np

def mape(y_true, y_pred):
    sum=0
    denom=0
    for index, value in enumerate(y_true):
        if value!=0:    
            sum+=abs((y_true[index]-y_pred[index])/y_true[index])
            denom+=1
    return (sum/denom)*100