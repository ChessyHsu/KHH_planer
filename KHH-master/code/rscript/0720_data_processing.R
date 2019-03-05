for(i in 1:nrow(sPilot)){
  if(!is.na(sPilot$tug3[i])){
    dPilot <- rbind(dPilot,sPilot[i,])
  }
}

zPilot <- zPilot[order(zPilot$num,zPilot$apply_time),]
dPilot <- data.frame()

dPilot <- zPilot[!is.na(zPilot$tug1),]

time <- data.frame(time=sTug$span[1],ship_num=sTug$ship_num[1],tug_num=sTug$tug_num[1],weight=dPilot$weight[1],front=dPilot$front_in_water[1],back=dPilot$back_in_water[1],status=sTug$status[1])
i <- 2
j <- 2
while (i <= nrow(dPilot) && j <= nrow(sTug)) {
  if(as.numeric(dPilot$num[i]) == as.numeric(sTug$ship_num[j]) && as.numeric(dPilot$status[i]) == as.numeric(sTug$status[j])){
    time <- rbind(time,time <- data.frame(time=sTug$span[j],ship_num=sTug$ship_num[j],tug_num=sTug$tug_num[j],weight=dPilot$weight[i],front=dPilot$front_in_water[i],back=dPilot$back_in_water[i],status=sTug$status[j]))
    i = i+1
    j = j+1
  }
  else if (as.numeric(dPilot$status[i]) != as.numeric(sTug$status[j])){
    j = j+1
  }
  else
    break
}

status <- vector(length = nrow(dPilot))
for(i in 1:nrow(dPilot)){
  if(dPilot$status[i]=="I")
    status[i] = 1
  else if(dPilot$status[i]=="T")
    status[i] = 2
  else if(dPilot$status[i]=="O")
    status[i] = 3
  else
    status[i] = 4
}
