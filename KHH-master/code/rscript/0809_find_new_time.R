starttime = rep(NA,nrow(tug))
for(i in 1:nrow(tug)) {
  if(is.na(tug$end_time[i])) next
  for(j in (1:nrow(vyg))[which(tug$shipID[i]==vyg$shipID)]) {
    if(tug$status[i]==1) {
      if(!is.na(vyg$in_port[j]) & format(vyg$in_port[j], format = "%Y%m%d") == tug$date[i]) {
        starttime[i] = vyg$in_port[j]
        break
      }
    }
    else if(tug$status[i]==2) {
      if(!is.na(vyg$trans[j]) & format(vyg$trans[j], format = "%Y%m%d") == tug$date[i]) {
        starttime[i] = vyg$trans[j]
        break
      }
    }
    else if(tug$status[i]==3) {
      if(!is.na(vyg$out_port[j]) & format(vyg$out_port[j], format = "%Y%m%d") == tug$date[i]) {
        starttime[i] = vyg$out_port[j]
        break
      }
    }
  }
}

worktime = rep(NA,nrow(tug))
worktime[!is.na(starttime)] = (tug$end_time - starttime)[!is.na(starttime)]
worktime = worktime/60
#worktime[is.na(worktime) | worktime>tug$total_time | worktime<0] = tug$total_time[is.na(worktime) | worktime>tug$total_time | worktime<0]
tug = cbind(shipID=tug$shipID,work_time=worktime, start_time=as.POSIXct(starttime, origin = "1970-01-01"),tug[,2:7])

ndf = data.frame()
for(i in 1:nrow(tug)) {
  c = which(tug$shipID[i]==df$shipID & tug$status[i]==df$status & format(tug$start_time[i],format="%Y%m%d")==df$date)
  if(length(c)==1){
    ndf = rbind(ndf, cbind(tug[i,1:5],df[c[1],c(5,7:20)]))
  }
}
