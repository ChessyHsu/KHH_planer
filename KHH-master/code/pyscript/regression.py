import pandas as pd
import numpy as np
import datetime
from sklearn import datasets, linear_model
from sklearn import cross_validation, linear_model
from sklearn.model_selection import train_test_split
from matplotlib import pyplot as plt
from sklearn.model_selection import KFold # import KFold
from sklearn.model_selection import cross_val_score, cross_val_predict
from sklearn import metrics
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

def mean_absolute_percentage_error(y_true, y_pred):
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100

def inregression():
	pd.set_option('display.max_columns', 100)
	df = pd.read_excel("main0916.xlsx")
	df = df.dropna(subset = ['work_time','pilot1','port','reverse','seven','day','weight_level','tug_cnt','dist','wind'])
	df = df[df.port != 0]
	df = df[df.port != 3]

	#choose in out or move
	df = df[df.sailing_status == 'I']

	#change to dummy variables
	df_weight = pd.get_dummies(df['weight_level'])
	df_port = pd.get_dummies(df['port'])
	df_port.columns = ['first_port','second_port']
	df_pilotID = pd.get_dummies(df['pilot1'])
	df_tugcnt = pd.get_dummies(df['tug_cnt'])
	df_tugcnt.columns = ['one_tug','two_tug','three_tug']

	#concat all the dependent variables
	newdf = pd.concat([df.work_time,df.dist, df.wind,df_weight,df_port,df.seven,df.day,df_pilotID,df_tugcnt,df.reverse], axis=1)
	newdf = pd.DataFrame(newdf)
	y = newdf.work_time
	newdf = newdf.drop(columns="work_time")

	#create training and testing vars
	X_train, X_test, y_train, y_test = train_test_split(newdf, y, test_size=0.2)

	#fit a model
	lm = LinearRegression()
	model = lm.fit(X_train, y_train)

	#Perform linear regression
	predictions = lm.predict(X_test)
	mse = np.mean((y_test - predictions) **2)
	mape = mean_absolute_percentage_error(y_test,predictions)
	print('MSE',mse,'MAPE',mape)
	print ("r^2:", model.score(X_test, y_test))
	# coef = lm.coef_
	# intercept = lm.intercept_
	# print(coef,intercept)

	# Perform 6-fold cross validation
	predictions = cross_val_predict(model, newdf, y, cv=100)
	mse_cross = np.mean((y-predictions)**2)
	mape_cross = mean_absolute_percentage_error(y,predictions)
	print('MSE',mse_cross,'MAPE',mape_cross)
	print ('Cross-Predicted r^2:', metrics.r2_score(y, predictions))

def outandtransregression(status):
	pd.set_option('display.max_columns', 100)
	df = pd.read_excel("main0916.xlsx")
	#get rid of NA and incorrect numbers
	df = df.dropna(subset = ['work_time','pilot1','port','seven','day','weight_level','tug_cnt','dist','wind'])
	df = df[df.port != 0]
	df = df[df.port != 3]
	df = df[df.sailing_status == status]
	#change to dummy variables
	df_weight = pd.get_dummies(df['weight_level'])
	df_port = pd.get_dummies(df['port'])
	df_port.columns = ['first_port','second_port']
	df_pilotID = pd.get_dummies(df['pilot1'])
	df_tugcnt = pd.get_dummies(df['tug_cnt'])
	df_tugcnt.columns = ['one_tug','two_tug','three_tug']
	#concat all the dependent variables
	newdf = pd.concat([df.work_time,df.dist, df.wind,df_weight,df_port,df.seven,df.day,df_pilotID,df_tugcnt], axis=1)
	newdf = pd.DataFrame(newdf)
	y = newdf.work_time
	newdf = newdf.drop(columns="work_time")
	#create training and testing vars
	X_train, X_test, y_train, y_test = train_test_split(newdf, y, test_size=0.2)
	#fit a model
	lm = LinearRegression()
	model = lm.fit(X_train, y_train)

	#Perform linear regression
	predictions = lm.predict(X_test)
	mse = np.mean((y_test - predictions) **2)
	mape = mean_absolute_percentage_error(y_test,predictions)
	print('MSE',mse,'MAPE',mape)
	# coef = lm.coef_
	# intercept = lm.intercept_
	# print(coef,intercept)
	print ("r^2:", model.score(X_test, y_test))

	# Perform 6-fold cross validation
	predictions = cross_val_predict(model, newdf, y, cv=100)
	mse_cross = np.mean((y-predictions)**2)
	mape_cross = mean_absolute_percentage_error(y,predictions)
	print('MSE',mse_cross,'MAPE',mape_cross)
	print ('Cross-Predicted r^2:', metrics.r2_score(y, predictions))
inregression()
outandtransregression('O')
outandtransregression('T')

