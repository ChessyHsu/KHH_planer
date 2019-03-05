# KHH
# 欄位以及資料放置位置

###### tags: `KHH` `Program` 
* 規範欄位名字
* 將所有欄位名稱所放的檔案
* 變數名稱為欄位名稱之開頭一律小寫
 變數名稱 tug_no


## 106年引水人動態看板.csv

| 欄位中文名稱 | 欄位英文名稱 | 變數型態|
| -------- | -------- | ------ |
| 船舶編號 | Tug_no | int |
| 引水人編號1| Pilot1_no | int  |
| 引水人編號2| Pilot2_no | int |
| 航行狀態1.2.3| Sailing_status| int/factor |
| 拖船編號1 | Tug1_no | int |
| 拖船編號2 | Tug2_no | int |
| 拖船編號3 | Tug3_no | int |
| 總噸位 | Total_weight | int |
| 前吃水 | Front_weight | int |
| 後吃水 | Back_weight | int |
| 靠泊狀態 | Parking_status | int/factor |

## 要額外 fetch 的欄位

| 欄位中文名稱 | 欄位英文名稱 | 變數型態 |
| -------- | -------- | -------|
| 工作時間 | Work_time | int |
| 移動時間 | Move_time | int |




## Variable definition
### 船舶
| 欄位中文名稱 | 變數名稱 | 
| -------- | -------- | 
| 船舶編號 | tug_no | int |
| 引水人編號1| pilot1_no | int  |
| 引水人編號2| pilot2_no | int |
| 航行狀態1.2.3| sailing_status| int/factor |
| 拖船編號1 | tug1_no | int |
| 拖船編號2 | tug2_no | int |
| 拖船編號3 | tug3_no | int |
| 總噸位 | total_weight | int |
| 前吃水 | front_weight | int |
| 後吃水 | back_weight | int |
| 靠泊狀態 | parking_status | int/factor |
| 拖船數目 | tug_cnt | int/factor |

End Variable definition


## 工作
- [ ] 計算任碼頭到港口間的距離 
- [ ] 將vyg的時間對上

