import pandas as pd
import numpy as np
import datetime
from sklearn import datasets, linear_model
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error
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
    return " + ".join("%s * %s\n" % (round(coef, 3), name)
                      for coef, name in lst)

def mean_absolute_percentage_error(y_true, y_pred):
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100

def regression(y_status,status,frameName):
	print(status,'\n')
	pd.set_option('display.max_columns', 100)
	df = pd.read_excel(frameName)
	df = df.dropna(subset = ['sailing_status',
							'pilot1',
							'tug_cnt',
							'front_weight',
							'back_weight',
							'weight_level',
							'pier_info',
							'dist',
							'wind',
							'reverse',
							'seven',
							'day',
							'avghp'])
	if status != 'T':
		df = df.dropna(subset = ['port'])
	df = df[df.port != 0]
	df = df[df.port != 3]
	df = df[df.max_work_time < 500]
	df = df[df.mean_work_time < 500]
	df = df[df.mean_work_time != 0]
	df = df[df.max_work_time != 0]
	df = df[df.min_work_time != 0]
	#choose in out or move
	df = df[df.sailing_status == status]

	#change to dummy variables
	df_port = pd.get_dummies(df['port'])
	df_port.columns = ['first_port','second_port']
	df_port.drop(columns = "second_port")
	df_pilotID = pd.get_dummies(df['pilot1'])
	df_tugcnt = pd.get_dummies(df['tug_cnt'])
	df_tugcnt.columns = ['one_tug','two_tug','three_tug']
	df_tugcnt.drop(columns = "three_tug")
	df_weight = pd.get_dummies(df['weight_level'])
	df_pier_info = pd.get_dummies(df['pier_info'])
	df_pier_info.columns = ['not_float','float']
	df_pier_info.drop(columns = "not_float")

	
	#concat all the dependent variables
	newdf = pd.concat([df_pilotID,
						df_tugcnt,
						df.front_weight,
						df.back_weight,
						df_weight,
						df_pier_info,
						df.dist,
						df.wind,
						df.reverse,
						df.seven,
						df.day], axis=1)

	if status != 'T':
		newdf = pd.concat([newdf,df_port],axis=1)
	newdf = pd.DataFrame(newdf)
	y = df[y_status]
	print(len(newdf.index))
	print(len(df[y_status].index))
	#create training and testing vars
	X_train, X_test, y_train, y_test = train_test_split(newdf, y, test_size=0.2)

	#lasso
	names = ['48','56','61','64','67','70','71','72','73','74','75','76','77','78','79','80','81','82','83','84','85','86','87','88','89','90','91','92','93','94','95','96','97','98','99','100','101','102','103','免',
			'one_tug','two_tug',
			'front_weight',
			'back_weight',
			'1','2','3','4','5','6','7','8',
			'float',
			'dist',
			'wind',
			'reverse',
			'seven',
			'day',
			'avghp',
			'first_port']
	minmse = 10000
	minmape = 100
	minmae = 10000
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
		mae = mean_absolute_error(y_test,predictions_lasso)
		if minmse > mse:
			num = i / 10000
		minmse = min(minmse,mse)
		minmape = min(minmape,mape)
		minmae = min(minmae,mae)
		
	print('MSE_l',minmse,'MAPE_l',minmape,'MAE_l',minmae)
	model_all = linear_model.Lasso(alpha= num, fit_intercept=True, normalize=True) # set parameters
	lasso = model_all.fit(X_train, y_train) # learn weights
	print("Lasso model:", pretty_print_linear(lasso.coef_,names=names,sort=True))
	print(lasso.score(X_train, y_train))

	#ridge
	clf = Ridge(alpha=1.0)
	ridge = clf.fit(X_train, y_train)
	predictions_ridge = ridge.predict(X_test)
	mse_r = np.mean((y_test - predictions_ridge) **2)
	mape_r = mean_absolute_percentage_error(y_test,predictions_ridge)
	mae_r = mean_absolute_error(y_test,predictions_ridge)
	print('MSE_r',mse_r,'MAPE_r',mape_r,'MAE_r',mae_r)
	print(ridge.score(X_train, y_train))
	print("Ridge model:", pretty_print_linear(ridge.coef_,names=names,sort=True))
#-----------------------------------------------------------
	#fit a model
	# lm = LinearRegression()
	# model = lm.fit(X_train, y_train)

	#importance
	# model_f = ExtraTreesClassifier()
	# model_f1 = model_f.fit(X_train, y_train)
	# print(model_f1.feature_importances_)

	#summary
	est = sm.OLS(y_train, X_train)
	est2 = est.fit()
	predictions_OLS = est2.predict(X_test)
	mse = np.mean((y_test - predictions_OLS) **2)
	mape = mean_absolute_percentage_error(y_test,predictions_OLS)
	print('MSE',mse,'MAPE',mape)
	print(est2.summary())


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
def describe_wait_time(status,frameName):
	pd.set_option('display.max_columns', 100)
	df = pd.read_excel(frameName)
	df = df.dropna(subset = ['sailing_status',
								'pilot1',
								'tug_cnt',
								'front_weight',
								'back_weight',
								'weight_level',
								'pier_info',
								'dist',
								'wind',
								'reverse',
								'seven',
								'day',
								'avghp'])
	df = df[df.sailing_status == status]
	df = df[df.pilot_wait_time < 500]
	print(df.pilot_wait_time.describe())
def mymean(status,frameName):
	print(status,'\n')
	pd.set_option('display.max_columns', 100)
	df = pd.read_excel(frameName)
	df = df.dropna(subset = ['sailing_status',
							'pilot1',
							'tug_cnt',
							'front_weight',
							'back_weight',
							'weight_level',
							'pier_info',
							'dist',
							'wind',
							'reverse',
							'seven',
							'day',
							'avghp'])
	if status != 'T':
		df = df.dropna(subset = ['port'])
	df = df[df.port != 0]
	df = df[df.port != 3]
	df = df[df.max_work_time < 500]
	df = df[df.mean_work_time < 500]
	df = df[df.mean_work_time != 0]
	df = df[df.max_work_time != 0]
	df = df[df.min_work_time != 0]
	#choose in out or move
	df = df[df.sailing_status == status]
	print(np.mean(df.max_work_time))

# regression('max_work_time','O','data/main1004.xlsx')
# describe_wait_time('I','data/main1004.xlsx',)
# describe_wait_time('O','data/main1004.xlsx',)
# describe_wait_time('T','data/main1004.xlsx',)
mymean('T','data/main1004.xlsx')
