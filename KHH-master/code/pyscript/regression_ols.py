import pandas as pd
import numpy as np
import datetime
from sklearn import datasets, linear_model
# from sklearn import cross_validation, linear_model
from sklearn.model_selection import train_test_split
from matplotlib import pyplot as plt
from sklearn.model_selection import KFold # import KFold
from sklearn.model_selection import cross_val_score, cross_val_predict
from sklearn import metrics
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import statsmodels.formula.api as sm
import statsmodels.api as sm
from scipy import stats
from sklearn.ensemble import ExtraTreesClassifier
import matplotlib.pyplot as plt

def pretty_print_linear(coefs, names=None, sort=False):
    if names == None:
        names = ["X%s" % x for x in range(len(coefs))]
    lst = zip(coefs, names)

    if sort:
        lst = sorted(lst, key=lambda x: -np.abs(x[0]))
    return " + ".join("%s * %s" % (round(coef, 3), name)
                      for coef, name in lst)

def mean_absolute_percentage_error(y_true, y_pred):
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100

def inregression(frameName):
	pd.set_option('display.max_columns', 100)
	df = pd.read_excel(frameName)
	df = df.dropna(subset = ['avghp','work_time','pilot1','reverse','seven','day','weight_level','tug_cnt','dist','wind'])
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
	newdf = pd.concat([df.avghp,df.dist,df_weight,df_pilotID,df_port,df.work_time,df.seven,df.day,df.wind,df_tugcnt,df.reverse], axis=1)
	newdf = pd.DataFrame(newdf)
	y = newdf.work_time
	testdf = newdf
	newdf = newdf.drop(columns="work_time")

	#create training and testing vars
	X_train, X_test, y_train, y_test = train_test_split(newdf, y, test_size=0.2)

	#lasso
	names = ['avghp',
					'dist',
					'1','2','3','4','5','6','7','8'
					'48','56','61','64','67','70','71','72','73','74','75','76','77','78','79','80','81','82','83','84','85','86','87','88','89','90','91','92','93','94','95','96','97','98','99','100','101','102','103','免'
					'first_port','second_port',
					'seven',
					'day',
					'wind',
					'one_tug','two_tug','three_tug'
					'reverse']
	minmse = 10000
	minmape = 100
	num = -1
	for i in range(0,1000,5):
		model_all = linear_model.Lasso(alpha= i/10000, fit_intercept=True, normalize=True) # set parameters
		lasso = model_all.fit(X_train, y_train) # learn weights
		# for i in range(30):
		# 	print('%.3f'%lasso.coef_[i])
		# print("Lasso model:", pretty_print_linear(lasso.coef_,names=names,sort=True))
		# print(lasso.score(X_train, y_train))

		predictions_lasso = lasso.predict(X_test)
		mse = np.mean((y_test - predictions_lasso) **2)
		mape = mean_absolute_percentage_error(y_test,predictions_lasso)
		if minmse > mse:
			num = i / 10000
		minmse = min(minmse,mse)
		minmape = min(minmape,mape)
	print(predictions_lasso)	
	print('MSE',minmse,'MAPE',minmape)
	model_all = linear_model.Lasso(alpha= num, fit_intercept=True, normalize=True) # set parameters
	lasso = model_all.fit(X_train, y_train) # learn weights
	print("Lasso model:", pretty_print_linear(lasso.coef_,names=names,sort=True))
	print(lasso.score(X_train, y_train))


#-----------------------------------------------------------
	#fit a model
	# lm = LinearRegression()
	# model = lm.fit(X_train, y_train)

	#importance
	# model_f = ExtraTreesClassifier()
	# model_f1 = model_f.fit(X_train, y_train)
	# print(model_f1.feature_importances_)

	#summary
	# est = sm.OLS(y_train, X_train)
	# est2 = est.fit()
	# predictions_OLS = est2.predict(X_test)
	# mse = np.mean((y_test - predictions_OLS) **2)
	# mape = mean_absolute_percentage_error(y_test,predictions_OLS)
	# print('MSE',mse,'MAPE',mape)
	# print(est2.summary())


	#Perform linear regression
	# predictions = lm.predict(X_test)
	# mse = np.mean((y_test - predictions) **2)
	# mape = mean_absolute_percentage_error(y_test,predictions)
	# print('MSE',mse,'MAPE',mape)
	# print ("r^2:", model.score(X_test, y_test))
	# coef = lm.coef_
	# intercept = lm.intercept_
	# print(coef,intercept)
#----------------------------------------------------------
	# Perform 6-fold cross validation
	# predictions = cross_val_predict(model, newdf, y, cv=100)
	# mse_cross = np.mean((y-predictions)**2)
	# mape_cross = mean_absolute_percentage_error(y,predictions)
	# print('MSE',mse_cross,'MAPE',mape_cross)
	# print ('Cross-Predicted r^2:', metrics.r2_score(y, predictions))

def outandtransregression(status,frameName):
	print(status,'\n')
	pd.set_option('display.max_columns', 100)
	df = pd.read_excel(frameName)
	#get rid of NA and incorrect numbers
	df = df.dropna(subset = ['avghp','work_time','pilot1','seven','day','weight_level','tug_cnt','dist','wind'])
	df = df[df.port != 0]
	df = df[df.port != 3]
	df = df[df.sailing_status == status]
	#change to dummy variables
	df_weight = pd.get_dummies(df['weight_level'])
	df_port = pd.get_dummies(df['port'])
	df_day = pd.get_dummies(df['day'])
	df_day.columns = ['night','day']
	df_port.columns = ['first_port','second_port']
	df_pilotID = pd.get_dummies(df['pilot1'])
	df_tugcnt = pd.get_dummies(df['tug_cnt'])
	df_tugcnt.columns = ['one_tug','two_tug','three_tug']
	#concat all the dependent variables
	newdf = pd.concat([df.wind,df.avghp,df.work_time,df.dist,df_weight,df_port,df.seven,df_pilotID,df_tugcnt,df.day,], axis=1)
	newdf = pd.DataFrame(newdf)
	y = newdf.work_time
	newdf = newdf.drop(columns=["work_time"])
	#create training and testing vars
	X_train, X_test, y_train, y_test = train_test_split(newdf, y, test_size=0.2)

	minmse = 10000
	minmape = 100
	num = -1
	names = ['avghp',
					'dist',
					'1','2','3','4','5','6','7',
					'48','56','61','64','67','70','71','72','73','74','75','76','77','78','79','80','81','82','83','84','85','86','87','88','89','90','91','92','93','94','95','96','97','98','99','100','101','102','103',
					'first_port',
					'seven',
					'day',
					'wind',
					'one_tug','two_tug']
	for i in range(0,1000,5):
		model_all = linear_model.Lasso(alpha= i/1000, fit_intercept=True, normalize=True) # set parameters
		lasso = model_all.fit(X_train, y_train) # learn weights
		# for i in range(30):
		# 	print('%.3f'%lasso.coef_[i])
		# print("Lasso model:", pretty_print_linear(lasso.coef_,names=names,sort=True))
		# print(lasso.score(X_train, y_train))

		predictions_lasso = lasso.predict(X_test)
		mse = np.mean((y_test - predictions_lasso) **2)
		mape = mean_absolute_percentage_error(y_test,predictions_lasso)
		if minmse > mse:
			num = i / 10000
		minmse = min(minmse,mse)
		minmape = min(minmape,mape)
	print(predictions_lasso)	
	print('MSE',minmse,'MAPE',minmape)
	model_all = linear_model.Lasso(alpha= num, fit_intercept=True, normalize=True) # set parameters
	lasso = model_all.fit(X_train, y_train) # learn weights
	print("Lasso model:", pretty_print_linear(lasso.coef_,names=names,sort=True))
	print(lasso.score(X_train, y_train))
	#fit a model
	# lm = LinearRegression()
	# model = lm.fit(X_train, y_train)



	# est = sm.OLS(y_train, X_train)
	# est2 = est.fit()
	# predictions_OLS = est2.predict(X_test)
	# mse = np.mean((y_test - predictions_OLS) **2)
	# mape = mean_absolute_percentage_error(y_test,predictions_OLS)
	# print('MSE',mse,'MAPE',mape)
	# print(est2.summary())

	#Perform linear regression
	# predictions = lm.predict(X_test)
	# mse = np.mean((y_test - predictions) **2)
	# mape = mean_absolute_percentage_error(y_test,predictions)
	# print('MSE',mse,'MAPE',mape)
	# coef = lm.coef_
	# intercept = lm.intercept_
	# print(coef,intercept)
	# print ("r^2:", model.score(X_test, y_test))

	# Perform 6-fold cross validation
	# predictions = cross_val_predict(model, newdf, y, cv=100)
	# mse_cross = np.mean((y-predictions)**2)
	# mape_cross = mean_absolute_percentage_error(y,predictions)
	# print('MSE',mse_cross,'MAPE',mape_cross)
	# print ('Cross-Predicted r^2:', metrics.r2_score(y, predictions))
inregression('data/main1010.xlsx')

outandtransregression('T','data/main1010.xlsx')
outandtransregression('O','data/main1010.xlsx')


