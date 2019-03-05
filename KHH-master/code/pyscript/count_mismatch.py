import pandas as pd

kanban_df = pd.read_excel('data/2017kanban.xlsx')
print(kanban_df.shape)

###Index(['船舶編號', '航次', '航行狀態(I進港O出港T移泊)', '引水申請時間', '引水人出發時間', '英文船名', '中文船名',
###       '港口(1/2)', '移泊地', '靠泊地', '引水人姓名1', '引水人姓名2', '拖船編號1', '拖船編號2', '拖船編號3',
###       '實際靠妥時間', '離開泊地時間', '港代理簡稱', '引水人上船時間', '引水人離船時間', '總噸位', '前吃水', '後吃水',
###       '靠泊狀況(L左靠，R右靠，0不指定)'],
###      dtype='object')
###
def tug_sd(tug_len,w):
    if w < 5000:
        if tug_len == 1: 
            standard = [117]
        else:
            standard = [117,117]
    elif w < 10000:
        if tug_len == 1:
            standard = [118]
        else:
            standard = [117,117]
    elif w < 15000:
        if tug_len == 1:
            standard = [118]
        else:
            standard = [117,118]
    elif w  < 30000:
        if tug_len == 1:
            standard = [119]
        else:
            standard = [118,119]
    elif w < 45000:
        if tug_len == 1:
            standard = [119]
        elif tug_len == 2:
            standard = [119,119]
        else:
            standard = [118,118,118]
    elif w < 60000:
        if tug_len == 1:
            standard = [120]
        elif tug_len == 2:
            standard = [120,120]
        else:
            standard = [120,120,120]
    elif w < 100000:
        if tug_len == 1:
            standard = [0]
        elif tug_len == 2:
            standard = [0,0]
        else:
            standard = [0,0,0]
    else:
        if tug_len == 1:
            standard = [0]
        elif tug_len == 2:
            standard = [0,0]
        else:
            standard = [0,0,0]
    
    return standard
            
  

 
for i in range(int(kanban_df.shape[0])):
    w = int(kanban_df.總噸位[i])
    tug = []
    tug.append(kanban_df.拖船編號1[i])
    tug.append(kanban_df.拖船編號2[i]) 
    tug.append(kanban_df.拖船編號3[i])
    tug = pd.series(tug)
    tug = tug.dropna()
    tug = pd.series.tolist(tug)

    tug_len = len(tug)
    mismatch = []
    standard = tug_sd(tug_len,w)
    for i in range(len(standard)):
        if(tug[i] < standard[i] and tug[i] is not 0 and standard[i] is not 0):
            mismatch.append(1)
            continue
        if i == len(standard) - 1:
            mismatch.append(0)
    print(mismatch)

        

