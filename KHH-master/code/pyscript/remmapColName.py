import sys
import pandas as pd
import os

def Fetch_VarName_dict(file_str):
    variable_file = open(file_str,"r")
    data = variable_file.read().split('\n')
    dict = {}
    start = True
    for i in range(len(data)):
        if "Variable defintion" in data[i] :
            start != start
        if start:
            if "End Variable defintion" in data[i]:
                start != start

            ## split the single line
            pair = data[i].split('|')
            ## filter the empty and the space string
            pair = list(filter(lambda item: item.strip(), pair))
            if len(pair) <= 2:
                continue

            ## Ignore the file
            key = pair[0].strip()
            value = pair[1].strip()

            dict[key] = value

    variable_file.close()
    return dict

## exec parsevarname.py in oeder to get the dictionary
## of variable name in defintion table of Variable.md
dict = Fetch_VarName_dict('../../Variable.md')



## Remmap the variable name of data frame
raw_data_path = "../../data/2017kanban.xlsx"
raw_df = pd.read_excel(raw_data_path)
raw_df.rename(columns=lambda x: dict.get(x), inplace=True)


head, tail = os.path.splitext(raw_data_path)
writer = pd.ExcelWriter(head+'_rehashed'+tail)
raw_df.to_excel(writer)
writer.save()

