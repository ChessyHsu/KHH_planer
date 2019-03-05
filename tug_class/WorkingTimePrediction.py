import numpy as np
import pandas as pd
import sklearn
import pickle
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
import os
#loc = os.path.dirname(__file__) + '/'
loc = 'C:/Users/user/Desktop/tug_class/tug_class/'

class WorkTimePrediction():
    """
    args:
        - data: Should be an one-row pandas.dataframe, and the columns include:
          sailing_status: "I", "O" or "T"
          port: 1 or 2
          tug_cnt: 1, 2 or 3
          total_weight: weight of the boat
          weight_level: weight level of the boat
          dist: distance of this work
          wind: wind of this hour
          park: "O", "L" or "R"
          reverse: 0 or 1
          month: month in number (1,2,3,...)
          hour: hour of the time
          avg_hp: average horsepower of the tug boat
    """
    def __init__(self, df): 
        with open(loc+'model_new/clf_1.pickle', 'rb') as f:
            self.clf1 = pickle.load(f)
        with open(loc+'model_new/clf_2.pickle', 'rb') as f:
            self.clf2 = pickle.load(f)
        with open(loc+'model_new/clf_3.pickle', 'rb') as f:
            self.clf3 = pickle.load(f)
        
        # regression model 
        with open(loc+'model_new/reg_1_0.pickle', 'rb') as f:
            self.reg1_0 = pickle.load(f)
        with open(loc+'model_new/reg_1_1.pickle', 'rb') as f:
            self.reg1_1 = pickle.load(f)
        with open(loc+'model_new/reg_2_0.pickle', 'rb') as f:
            self.reg2_0 = pickle.load(f)
        with open(loc+'model_new/reg_2_1.pickle', 'rb') as f:
            self.reg2_1 = pickle.load(f)
        with open(loc+'model_new/reg_3_0.pickle', 'rb') as f:
            self.reg3_0 = pickle.load(f)
        with open(loc+'model_new/reg_3_1.pickle', 'rb') as f:
            self.reg3_1 = pickle.load(f)
        
        self.df = df
        self.data = pd.DataFrame([[0]*58],\
                                 columns= list(['total_weight', 'weight_level', 'dist', 'wind', 'avg_hp', \
                                "['port']_1", "['port']_2", "['tug_cnt']_1", "['tug_cnt']_2", "['tug_cnt']_3", \
                                "['park']_l", "['park']_o", "['park']_r", "['reverse']_0","['reverse']_1", \
                                "['month']_1", "['month']_2", "['month']_3","['month']_4", \
                                "['month']_5", "['month']_6", "['month']_7","['month']_8", \
                                "['month']_9", "['month']_10", "['month']_11","['month']_12", \
                                "['hour']_0", "['hour']_1", "['hour']_2", "['hour']_3", \
                                "['hour']_4", "['hour']_5", "['hour']_6", "['hour']_7", "['hour']_8", \
                                "['hour']_9", "['hour']_10", "['hour']_11", "['hour']_12", \
                                "['hour']_13", "['hour']_14", "['hour']_15", "['hour']_16", \
                                "['hour']_17", "['hour']_18", "['hour']_19", "['hour']_20", \
                                "['hour']_21", "['hour']_22", "['hour']_23", "['weekday']_0", \
                                "['weekday']_1", "['weekday']_2", "['weekday']_3", "['weekday']_4", \
                                "['weekday']_5", "['weekday']_6"]))

        self.status = "none"
        self.dm_col = ["port", "tug_cnt", "park", "reverse", "month", "hour", "weekday"]
        self.pr_col = ["dist", "weight_level", "total_weight", "wind", "avg_hp"]
        
    
    def preprocessing(self):
        for i in self.pr_col:
            self.data.iloc[0][i] = self.df[i][0]
                                      
        # to categorical
        for i in self.dm_col:
            self.data.iloc[0][ "['" + i + "']_" + str(self.df.iloc[0][i]) ] = 1
   
        if self.df["sailing_status"][0] == "I":
            self.status = "i"
        elif self.df["sailing_status"][0] == "T":
            self.status = "t"
        elif self.df["sailing_status"][0] == "O":
            self.status = "o"

    def predict(self):
        if self.status == "i":
            # predict whether larger or smaller than median (35)
            pred_clf = self.clf1.predict(self.data)
            if pred_clf == 0:
                pred_reg = self.reg1_0.predict(self.data)
            else:
                pred_reg = self.reg1_1.predict(self.data)
        
        elif self.status == "t":
            # predict whether larger or smaller than median (42)
            pred_clf = self.clf2.predict(self.data)
            if pred_clf == 0:
                pred_reg = self.reg2_0.predict(self.data)
            else:
                pred_reg = self.reg2_1.predict(self.data)
        else:
            # predict whether larger or smaller than median (15)
            pred_clf = self.clf3.predict(self.data)
            if pred_clf == 0:
                pred_reg = self.reg3_0.predict(self.data)
            else:
                pred_reg = self.reg3_1.predict(self.data)
        
        return pred_reg
    
    def run(self):
        self.preprocessing()
        pred_time = self.predict()
        # print(pred_time)
        return pred_time

# df = pd.read_excel('C:/Users/user/Desktop/KHH-master/KHH-master/code/pyscript/data/cher1218.xlsx')
# print(df)

# result=open("predict_y2.csv", 'w')
# title=["sailing_status", "port", "tug_cnt", "total_weight", "weight_level", "dist", "wind", "park", \
#                                   "reverse", "month", "weekday", "hour", "avg_hp"]

# for i in range(len(df)):
#     print(i)
#     print("---------------------")
#     row=[]
#     for t in title:
#         row.append(df.loc[i,t])
#     df1=pd.DataFrame([row],columns=list(title))
#     wt = WorkTimePrediction(df1)
#     y2=wt.run()
#     print(y2[0])
#     result.write(str(y2[0])+"\n")
# result.close()

# df = pd.DataFrame([["T",1,1,27968,4,1502.6, 1,"L",0,1,1,21,5200]], \
#                   columns = list(["sailing_status", "port", "tug_cnt", "total_weight", "weight_level", "dist", "wind", "park", \
#                                   "reverse", "month", "weekday", "hour", "avg_hp"]))


# wt1 = WorkTimePrediction(df)
# print ("------wktime:",wt1.run(),"------")

