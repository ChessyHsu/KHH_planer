"""interface for access existing data
"""

# read excel data
import pandas as pd
# harbor to pier distance
df_port_to_pier = pd.read_excel("data/complete_dis.xlsx",index_col = "代號")
#pier to pier distance
df_pier_to_pier = pd.read_excel("data/complete_dis_meter.xlsx",index_col = 1)

#reverse: if 'L' then 0 順 1 逆
df_reverse1 = pd.read_excel("data/左靠逆靠.xlsx")


def get_portToPier_dist(port,pier):
    portnum = 9001 if port == 1 else 9002
    return (df_port_to_pier.loc[int(portnum),int(pier)])

def get_pierToPier_dist(pier1, pier2):
    return df_pier_to_pier.loc[int(pier1),int(pier2)]


def get_pier_lanlng(pier):
    if pier == 9001:
        return (22.616677,120.265942)
    elif pier == 9002:
        return (22.552638,120.316716)

    return tuple([float(i) for i in df_port_to_pier.loc[int(pier),"經緯度"].split(',')])

def get_reverse(task):
    reverse = 0
    if task.ship_state == 'I':
        if task.start == 9001:
            if task.side == 'L':
                reverse = bool(df_reverse1.loc[int(task.to),9001])
            else:
                reverse = not(bool(df_reverse1.loc[int(task.to),9001]))
        elif task.start == 9002:
            if task.side == 'L':
                reverse = bool(df_reverse1.loc[int(task.to),9002])
            else:
                reverse = not(bool(df_reverse1.loc[int(task.to),9002]))
    elif task.ship_state == 'T':

        reverse = 0
    return reverse
