import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

dic = {
    "type":["training", "testing"],
    "linear_regression":[],
    "random_forest":[],
    "Adaboost":[],
    "support_vector_regression":[]
}
df = pd.DataFrame(dic)
index = np.arange(2)

A = df[df.type=="training"]["linear_regression"]
B = df[df.type=="testing"]["linear_regression"]
