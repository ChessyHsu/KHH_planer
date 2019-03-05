
# coding: utf-8

# # 計算工作時間
# 
# * kanban 紀錄各船舶相關資訊，包含噸位、前後吃水
# * vyg 記錄拖船開始工作時間
#     * 進港 = 進港港口通過時間
#     * 移泊 = 移泊移動開始時間
#     * 出港 = 內港離開時間
# * tug 記錄拖船結束工作時間
# 
# **use** ```jupyter nbconvert --to script count_worktime.ipynb``` **to export to script**

# In[1]:


import pandas as pd
pd.set_option('display.max_columns', 100)

kanban = pd.read_excel("data/2017kanban.xlsx")
vyg = pd.read_excel("data/2017vyg.xlsx")
tug = pd.read_excel("data/2017tug.xlsx")


# ## 首先從 kanban 獲得引水申請時間

# In[2]:


kanban.rename(columns={"航行狀態(I進港O出港T移泊)" : "航行狀態", "靠泊狀況(L左靠，R右靠，0不指定)":"靠泊"}, inplace=True)


# In[3]:


kanban = (kanban[
            kanban.拖船編號1.notnull() &
            kanban.靠泊地.notnull() &
            ((kanban.航行狀態 != 'T') | (kanban.移泊地.notnull())) &
            ((kanban.航行狀態 == 'T') | (kanban['港口(1/2)'] == 1) | (kanban['港口(1/2)'] == 2))
        ].reset_index(drop=True))


# In[4]:


kanban.head()


# In[5]:


from datetime import datetime, timedelta
def adjust_apply_time(s):
    t = datetime.strptime('0'+s, "%Y/%m/%d %H:%M:%S")
    return t.replace(year=t.year+1911)
    
apply_time = kanban.引水申請時間.map(adjust_apply_time)
kanban = (kanban.assign(apply_time=apply_time)
                .assign(航次=kanban.航次.map(lambda no: int(no)))
         )


# ## 接著從vyg找出拖船作業開始時間並貼上

# In[6]:


vyg.head()


# In[7]:


vyg.船舶編號 = vyg.船舶編號.map(lambda no: int(no.strip('_').strip('X')))    


# In[8]:


def match_start_time(row):
    start = pd.Series()
    if row.航行狀態 == 'I':
        start = vyg.loc[(vyg.船舶編號 == row.船舶編號) & (vyg.航次 == row.航次), '進港港口通過時間'].dropna()
    elif row.航行狀態 == 'O':
        start = vyg.loc[(vyg.船舶編號 == row.船舶編號) & (vyg.航次 == row.航次), '內港離開時間'].dropna()
    elif row.航行狀態 == 'T':
        start = vyg.loc[(vyg.船舶編號 == row.船舶編號) & (vyg.航次 == row.航次), '移泊移動開始時間'].dropna()
    
    if start.empty:
        return None
    
    if start.count() > 1:
        return -1
    
    return start.iloc[0]


kanban = kanban.assign(start_time=kanban.apply(match_start_time, axis=1))


# In[9]:


def match_ready_time(row):
    ready = pd.Series()
    if row.航行狀態 == 'I':
        ready = vyg.loc[(vyg.船舶編號 == row.船舶編號) & (vyg.航次 == row.航次), '防波堤通過時間（進）'].dropna()
    elif row.航行狀態 == 'O':
        ready = vyg.loc[(vyg.船舶編號 == row.船舶編號) & (vyg.航次 == row.航次), '申請出港時間'].dropna()
    elif row.航行狀態 == 'T':
        ready = vyg.loc[(vyg.船舶編號 == row.船舶編號) & (vyg.航次 == row.航次), '移泊移動申請時間'].dropna()
    
    if ready.empty:
        return None
    
    if ready.count() > 1:
        return -1
    
    return ready.iloc[0]


kanban = kanban.assign(pilot_ready_time=kanban.apply(match_ready_time, axis=1))


# In[10]:


kanban = (kanban[kanban.start_time.notnull() & 
                 kanban.pilot_ready_time.notnull() & 
                (kanban.start_time != -1) &
                (kanban.pilot_ready_time != -1)
               ].reset_index(drop=True))


# ## 最後從tug中找出工作結束時間並貼上

# In[11]:


end_time = tug.apply(lambda df: datetime.strptime(str(df.報告日期).zfill(8) + " " + str(df.終止時分).zfill(4), "%Y%m%d %H%M"), axis="columns")
tug_start = tug.apply(lambda df: datetime.strptime(str(df.報告日期).zfill(8) + " " + str(df.開始時分).zfill(4), "%Y%m%d %H%M"), axis="columns")
ship_no = tug.高港船舶編號.map(lambda s: int(s))
tug = tug.assign(end_time=end_time).assign(start_time=tug_start).assign(ship_no=ship_no)


# In[12]:


import numpy as np

size = len(kanban)
min_end_time = pd.Series([None] * size)
min_work_time = pd.Series([None] * size)
max_end_time = pd.Series([None] * size)
max_work_time = pd.Series([None] * size)
mean_work_time = pd.Series([None] * size)

def match_end_time():
    i = 0
    while (i < size):
        row = kanban.iloc[i]
        df = tug.loc[(tug.ship_no == row.船舶編號) & (tug.航次 == row.航次) & (tug.status == row.航行狀態), 'end_time']
        if not df.empty:
            min_end_time[i] = np.min(df)
            min_work_time[i] = min_end_time[i]-row.start_time
            max_end_time[i] = np.max(df)
            max_work_time[i] = max_end_time[i]-row.start_time
            mean_work_time[i] = np.mean(df-row.start_time)
        i += 1


# In[13]:


match_end_time()


# In[14]:


kanban = (kanban.assign(
                min_end_time   = min_end_time, 
                min_work_time  = min_work_time, 
                max_end_time   = max_end_time, 
                max_work_time  = max_work_time, 
                mean_work_time = mean_work_time, 
            ))


# In[15]:


kanban = (kanban[kanban.start_time.notnull() & 
                 kanban.min_work_time.notnull() & 
                 kanban.min_end_time.notnull() & 
                 kanban.max_work_time.notnull() & 
                 kanban.max_end_time.notnull() & 
                 kanban.mean_work_time.notnull() &
                 (kanban.min_work_time >= timedelta(0)) &
                 (kanban.max_work_time >= timedelta(0))
                ].reset_index(drop=True))


# ## 計算拖船數量、噸位層級、平均風力

# In[16]:


wind = pd.read_csv("data/avg_weather.csv")


# In[17]:


import numpy as np

def classify_weight_level(w):
    level = {5000: 1, 10000: 2, 15000: 3, 30000: 4, 45000: 5, 60000: 6, 100000: 7}
    for k in level:
        if w < k:
            return level[k]
    return 8

def fetch_wind(t):
    w = wind[(wind.date == int(t.strftime("%Y%m%d"))) & (wind.hour == int(t.strftime("%H")))].power
    return None if w.empty else w.item()

kanban = (kanban
     .assign(tug_cnt = kanban.apply(lambda row: 3 - np.isnan(row.拖船編號1) - np.isnan(row.拖船編號2) - np.isnan(row.拖船編號3), axis=1))
     .assign(weight_lv = kanban.總噸位.map(classify_weight_level))
     .assign(wind = kanban.start_time.map(fetch_wind))
)


# In[18]:


kanban = kanban[kanban.wind.notnull()].reset_index(drop=True)


# ## 計算作業距離

# In[19]:


dist_pier = pd.read_excel('data/complete_dis_meter.xlsx', index_col=1)

def fetch_dist(row):
    if row.航行狀態 == 'I' or row.航行狀態 == 'O':
        if pd.isnull(row.靠泊地) or pd.isnull(row['港口(1/2)']) or int(row.靠泊地) not in dist_pier.index:
            return None
        return dist_pier.loc[int(row.靠泊地), 9001] if int(row['港口(1/2)']) == 1 else dist_pier.loc[int(row.靠泊地), 9002]
    elif row.航行狀態 == 'T':
        if pd.isnull(row.靠泊地) or pd.isnull(row.移泊地) or int(row.靠泊地) not in dist_pier.index or int(row.移泊地) not in dist_pier.index:
            return None
        return dist_pier.loc[int(row.移泊地), int(row.靠泊地)]
        

kanban = kanban.assign(dist = kanban.apply(fetch_dist, axis=1))
kanban = kanban[kanban.dist.notnull()].reset_index(drop=True)


# ## 辨識順逆靠
# 
# **註：移泊和出港等有資料才能做**

# In[20]:


kanban['靠泊'] = kanban['靠泊'].replace({'0':'O', 'N':'O'})
pd.set_option('mode.chained_assignment', None)


# In[21]:


# 讓出港前最後一次的的靠泊狀況以出港為準
kanban2 = kanban.iloc[0:1]
indexes = kanban.船舶編號.value_counts().index
for idx in indexes:
    df = kanban[kanban.船舶編號 == int(idx)].reset_index()
    i = 0
    while i < len(df):
        j = i
        while j < (len(df)-1) and df.iloc[j].航次 == df.iloc[j+1].航次:
            j += 1
        if (j > 0 and 
            df.iloc[j].航行狀態 == 'O' and 
            df.iloc[j].靠泊 != 'O' and 
            df.iloc[j].航次 == df.iloc[j-1].航次 and 
            df.iloc[j].靠泊 != df.iloc[j-1].靠泊):
            df.loc[j-1, '靠泊'] = df.loc[j, '靠泊']
        i = j + 1
    kanban2 = pd.concat([kanban2, df], sort=False)


# In[22]:


temp_kanban = kanban
kanban = kanban2


# In[23]:


turn = pd.read_excel('data/左靠逆靠.xlsx', index_col=0)


# In[24]:


turn_pier = pd.read_excel('data/移泊順逆靠.xlsx', index_col=0)


# In[25]:


def fetch_reverse(row):
    table = {"RR": 0, "RL": 1, "LR": 2, "LL": 3, "RO": 4, "LO": 5, }

    # 進港和出港找不到碼頭都當順靠
    if int(row.靠泊地) not in turn.index:
        return 0
    
    if row.航行狀態 == 'O':
        if row.靠泊 == 'R':
            return turn.loc[int(row.靠泊地), 9001] if row['港口(1/2)'] == 1 else turn.loc[int(row.靠泊地), 9002]
        elif row.靠泊 == 'L':
            return 1 - turn.loc[int(row.靠泊地), 9001] if row['港口(1/2)'] == 1 else 1 - turn.loc[int(row.靠泊地), 9002]
    
    if row.航行狀態 == 'I':
        if row.靠泊 == 'L':
            return turn.loc[int(row.靠泊地), 9001] if row['港口(1/2)'] == 1 else turn.loc[int(row.靠泊地), 9002]
        elif row.靠泊 == 'R':
            return 1 - turn.loc[int(row.靠泊地), 9001] if row['港口(1/2)'] == 1 else 1 - turn.loc[int(row.靠泊地), 9002]
        
    if row.航行狀態 == 'T':
        if int(row.移泊地) not in turn_pier.index or int(row.靠泊地) not in turn_pier.index:
            return 0
        else:
            last = kanban[(kanban.船舶編號 == row.船舶編號) & (kanban.航次 == row.航次) & (kanban.start_time < row.start_time)]
            if not last.empty:
                last = last.iloc[-1]
                ps = str(last.靠泊) + str(row.靠泊)
                best = turn_pier.loc[int(row.移泊地), int(row.靠泊地)]
                if np.isnan(best):
                    return 0
                if ((ps == 'RR' and best == 0) or
                    (ps == 'RL' and best == 1) or
                    (ps == 'LR' and best == 2) or
                    (ps == 'RL' and best == 3) or
                    (last.靠泊 == 'R' and best == 4) or
                    (last.靠泊 == 'L' and best == 5) or
                    (row.靠泊 == 'R' and best == 6) or
                    (row.靠泊 == 'L' and best == 7)):
                    return 0
                else:
                    return 1
    return 0

kanban = kanban.assign(reverse = kanban.apply(fetch_reverse, axis=1))


# ## 碼頭資訊

# In[26]:


pier_info = pd.read_excel('data/pier_info.xlsx')


# In[27]:


def fetch_pier_info(row):
    if int(row.靠泊地) in pier_info.index:
        return pier_info.loc[int(row.靠泊地), 'info']
    return 0

kanban = kanban.assign(pier_info = kanban.apply(fetch_pier_info, axis=1))


# ## 匯出成main<當日日期>.xlsx

# In[28]:


kanban = kanban.iloc[1:].sort_values('apply_time').reset_index(drop=True)


# In[32]:


main = pd.DataFrame({
    'ship_no':          kanban.船舶編號,
    'sailing_status':   kanban.航行狀態,
    'min_work_time':    (kanban.min_work_time / np.timedelta64(1, 'm')).round(),
    'max_work_time':    (kanban.max_work_time / np.timedelta64(1, 'm')).round(),
    'mean_work_time':   (kanban.mean_work_time / np.timedelta64(1, 'm')).round(),
    'start_time':       kanban.start_time,
    'min_end_time':     kanban.min_end_time,
    'max_end_time':     kanban.max_end_time,
    'pilot_ready_time': kanban.pilot_ready_time,
    'pilot_wait_time':  pd.concat([pd.Series(((kanban.start_time - kanban.pilot_ready_time) / np.timedelta64(1, 'm')).values).round(),
                                    pd.Series([0] * len(kanban))], axis=1).max(axis=1),
    'port':             kanban['港口(1/2)'],
    'place1':           kanban.移泊地,
    'place2':           kanban.靠泊地,
    'pilot1':           kanban.引水人姓名1,
    'pilot2':           kanban.引水人姓名2,
    'tug1_no':          kanban.拖船編號1,
    'tug2_no':          kanban.拖船編號2,
    'tug3_no':          kanban.拖船編號3,
    'tug_cnt':          kanban.tug_cnt,
    'total_weight':     kanban.總噸位,
    'front_weight':     kanban.前吃水,
    'back_weight':      kanban.後吃水,
    'weight_level':     kanban.weight_lv,
    'pier_info':        kanban.pier_info,
    'dist':             kanban.dist,
    'wind':             kanban.wind,
    'park':             kanban.靠泊,
    'reverse':          kanban.reverse,
    'seven':            kanban.start_time.map(lambda t:int(int(t.strftime("%H")) == 7)),
    'day':              kanban.start_time.map(lambda t:int(int(t.strftime("%H")) > 5 and int(t.strftime("%H")) < 19)),
})


# In[33]:


main.to_excel("data/khh"+datetime.now().strftime("%m%d")+".xlsx", index=False)

