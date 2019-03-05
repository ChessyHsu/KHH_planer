library(readxl)
setwd("Documents/Project")
df = read_excel("xlsx/Info.xlsx")
df1 = read_excel("xlsx/tugInfo.xlsx")
df = df[with(df,order(df$船舶編號,df$引水申請時間)),]
df1 = df1[with(df1,order(df1$高港船舶編號,df1$報告日期)),]
df[,13] = c()
name = df1[1,]$船舶編號
bb = TRUE;
for(i in 1:nrow(df)){
  for(l in 1:nrow(df1)){
    if (df[i,]$船舶編號 == df1[l,]$高港船舶編號) #船舶no
    {
      bb = FALSE;
      if(df[i,]$引水申請時間 == df1[l,]$報告日期)#日期
      {
        if(df[i,]$`航行狀態(1進港3出港2移泊)` == df1[l,]$`1：進港\r\n2：移泊\r\n3：出港\r\n4：其他\r\n`) # in,out
        {
          df[i,13] <- df1[l,9] 
        }
      }
    }else{
      
      if(bb == FALSE)
      {
        bb = TRUE;
        break;
      }
    }
  }
}
