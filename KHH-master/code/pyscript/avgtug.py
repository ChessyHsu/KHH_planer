#!/usr/bin/env python
# coding: utf-8

# In[101]:



import pandas as pd
pd.set_option('display.max_columns', 100)


main0 = pd.DataFrame( pd.read_excel("data/khh1005.xlsx"))


# In[102]:


def tug_to_hp(no):
    ##缺568拖船資訊
    tuginfo = {143: 1800,
               145: 1800,
               151: 2400,
               152: 2400,
               153: 2400,
               155: 2400,
               112: 2400,
               241: 2400,
               245: 2400,
               321: 3200,
               322: 3200,
               101: 3200,
               302: 3200,
               104: 3200,
               106: 3200,
               108: 3200,
               109: 3200,
               303: 3300,
               306: 3400,
               308: 3500,
               301: 3600,
               161: 4000,
               162: 4000,
               163: 4200,
               165: 4200,
               401: 4400,
               451: 4500,
               171: 5200,
               172: 5200,
               181: 6400,
               182: 6400}
    for k in tuginfo:
        if no == k:
            return tuginfo[k]
   return null


# In[112]:


# import numpy as np
# print(main0.head())
# n = len(main0)
# tug1 = pd.Series(main0.tug1_no)
# tug2 = pd.Series(main0.tug2_no)
# tug3 = pd.Series(main0.tug3_no)

# tug2.isna()
# avghp = pd.Series([],name = "avgtug")


# for i in range(n):
#     ## only 1 tug
#     if pd.isna(tug2[i]) and pd.isna(tug3[i]):
#         avghp[i] = tug_to_hp(tug1[i])
#     ## 2 tugs
#     elif pd.notna(tug2[i]) and pd.isna(tug3[i]):
#         avghp[i] = (tug_to_hp(tug1[i])+tug_to_hp(tug2[i]))/2
#     ## 3 tugs
#     else:
#         avghp[i] = (tug_to_hp(tug1[i])+tug_to_hp(tug2[i])+tug_to_hp(tug3[i]))/3
# print(avghp)


# In[113]:


avghp = pd.Series(avghp,name = "avg_hp")
main1 = main0.join(avghp)
print(main1.tail())


# # In[114]:


writer = pd.ExcelWriter('data/khh1005.xlsx')
main1.to_excel(writer,'Sheet1')
writer.save()


# In[ ]:




