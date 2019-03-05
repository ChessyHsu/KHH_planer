import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import statsmodels.api as sm

def mean_absolute_percentage_error(y_true, y_pred):
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    return np.mean(np.abs((y_true - y_pred) / y_true))

### read file
df = pd.read_excel("data/main1004.xlsx")

df = df[(df.sailing_status == 'T') | 
        ((df.sailing_status == 'I') | (df.sailing_status == 'O') & 
         (df.port == 1) | (df.port == 2))]


# change to dummy variables
df_weight = pd.get_dummies(df['weight_level'])
df_port = pd.get_dummies(df['port'])
df_port.columns = ['_', 'port1','port2']
df_pilotID = pd.get_dummies(df['pilot1'])
df_tugcnt = pd.get_dummies(df['tug_cnt'])
df_pier_info = pd.get_dummies(df['pier_info'])

# concat all the dependent variables
newdf = pd.concat([
            pd.DataFrame({
#                'weight'    : df.total_weight,
                'dist'      : df.dist,
#                'wind'      : df.wind,
                'avghp'     : df.avghp,
                'seven'     : df.seven,
                'day'       : df.day,
                'reverse'   : df.reverse,
            }),
            df_weight.iloc[:,:-1],
            df_port.iloc[:,1],
            df_pilotID.iloc[:,:-1],
            df_tugcnt.iloc[:,:-1].rename(columns={1: 'one_tug', 2: 'two_tugs'}),
            df_pier_info.iloc[:,:-1].rename(columns={0: 'normal_pier'}),            
        ], axis=1)

y = df.min_work_time

def do_regression(msg, x, y):
    
    # split training and testing sets
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)
    
    # do regression
    est = sm.OLS(y_train, x_train).fit()
    predictions = est.predict(x_test)
    
    # calculate errors
    mse = np.mean((y_test - predictions) ** 2)
    mae = np.mean(np.abs(y_test - predictions))
    mape = mean_absolute_percentage_error(y_test, predictions)
    
    # print result
    print("\n\n{}{}{}\n".format("# "*17, msg.center(10), "# "*17))
    print("MSE: {:.4f}\tMAE: {:.4f}\tMAPE: {:.4%}\n".format(mse, mae, mape))
    print(est.summary())

do_regression(
        'IN',
        newdf[(df.sailing_status == 'I')], 
        y[df.sailing_status == 'I']
)

do_regression(
        'TRANSFER',
        newdf[df.sailing_status == 'T'].drop(columns=['port1']), 
        y[df.sailing_status == 'T']
)

do_regression(
        'OUT',
        newdf[(df.sailing_status == 'O') & (df.min_work_time > 0)], 
        y[(df.sailing_status == 'O') & (df.min_work_time > 0)]
)