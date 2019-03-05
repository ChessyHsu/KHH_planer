import pandas as pd
import math
import numpy as np

def haversine(lon1, lat1, lon2, lat2):
  lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])
  dlon = lon2 - lon1
  dlat = lat2 - lat1
  a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
  c = 2 * math.asin(math.sqrt(a))
  r = 6371
  return c * r * 1000

def formula(dis):
    return (dis) / 1852 * 60 / 10

pos_pier_path = 'data/pos_of_pier.xlsx'
pos = pd.read_excel(pos_pier_path)
pos_df = pd.DataFrame(pos)

pos = pos_df["經緯度"]
pier_no = pos_df["代號"]
dis_colname = ['pier_no']+ list(pier_no)

def count_dis(path=""):
    dis_df = pd.DataFrame(pier_no)
    for i in range(len(pos)) :
        dis = []
        if(str(pos[i]) == 'nan'):
            dis_df = pd.concat([dis_df,pd.Series([''] * len(pos))],axis=1)
            continue
        base_lng = float(str(pos[i]).split(',')[0])
        base_lat = float(str(pos[i]).split(',')[1])
        for j in range(len(pos)):
            p = str(pos[j])
            if(p == 'nan'):
                dis.append('')
                continue
            lng = float(p.split(',')[0])
            lat = float(p.split(',')[1])
            dis.append(haversine(lng,lat,base_lng,base_lat))
        dis_df = pd.concat([dis_df,pd.Series(dis)],axis=1)
    dis_df.columns = dis_colname
    if(path != ""):
        writer = pd.ExcelWriter(path)
        dis_df.to_excel(writer)
        writer.save()
    return dis_df

def count_time(dis_df_path ,path=""):
    dis_df = pd.read_excel(dis_df_path)
    time_df = pd.DataFrame(pier_no)
    for i in range(len(pier_no)):
        time = []
        for j in range(1,len(pier_no)):
            if(str(dis_df.iloc[i,j]) == ""):
                time.append('')
                continue
            time.append(formula(dis_df.iloc[i,j]))
        time_df = pd.concat([time_df,pd.Series(time)],axis = 1)
    time_df.columns = dis_colname
    if(path != ""):
        writer = pd.ExcelWriter(path)
        time_df.to_excel(writer)
        writer.save()

    return time_df

def main():
    
    #count_time('data/complete_dis_meter.xlsx', 'data/complete_time_min.xlsx')
    df = pd.read_excel('data/complete_time_min.xlsx')
    df = pd.DataFrame(df)
    print(df)
    df = df.iloc[:,1:int(df.shape[1])]
    print(df.describe())

    ## the time of pier
    des = df.describe().iloc[0:int(df.shape[0] - 3),0:int(df.shape[1] - 3)]
    mean = des.iloc[1,:]
    ma = des.iloc[7,:].max()
    mm = des.iloc[3,:].min()
    sd = des.iloc[2,:]

    ## Count the standard deviation
    ds = df.iloc[0:int(df.shape[0] - 2), 0: int(df.shape[1] - 2)]
    #print(ds)
    #print(ds.values)

    val = ds.values
    val = val[~np.isnan(val)]
    print(np.std(val))
    #print(mm)
    #print(ma)
    #print(des.iloc[2,:].mean())
    ##





if __name__ == "__main__":
    main()
