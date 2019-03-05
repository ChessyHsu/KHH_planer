for(i in 1:length(index)){
  p[pilot1==index[i],i] <- 1
}
  
for(i in 0:23) {
  hours[nt==i,(i+1)] <- 1
}

count <- c("05","06","07","08","09",as.character(10:23))

j = 0
for(i in count) {
  nt[pilot$hour==i] <- 5+j
  j = j+1
}

for(i in 1:length(port1.power)) {
  if(port1.power[i] == 100) {
    port1.power[i] = port2.power[i]
  }
}

df1 <- nndf[nndf$status==1,]
x1 <- cbind(df1[,6:10],df1[,12:50],df1[,57:58])
lm1 <- lm(df1$worktime~data.matrix(x1))
summary(lm1)

port1.t <- rep(-1,365*26)
port2.t <- rep(-1,365*26)
wtime <- rep(-1,365*26)
wdate <- rep(-1,365*26)
j = 1
k = 1
for(i in 2:nrow(weather)) {
  if(wwtime[i] != wwtime[i-1]) {
    port1.t[k] = mean(weather$port1.t[j:(i-1)])
    port2.t[k] = mean(weather$port2.t[j:(i-1)])
    wtime[k] = wwtime[i-1]
    wdate[k] = wwdate[i-1]
    k = k+1
    j = i
  }
}

m1 <- mean(wind$gust1)
m2 <- mean(wind$gust2)
for(i in 1:length(gust)) {
  if(gust[i] == -1) {
    if(port2 == 1) {
      gust[i] = m2
    }
    else {
      gust[i] = m1
    }
  }
}

front.d <- rep(0,length(newdf$front))
for(i in 1:length(newdf$front)) {
  front.d[i] <- as.double(newdf$front[i])
}

port1 <- rep(0,36251)
port2 <- rep(0,36251)
port1[port==1] <- 1
port2[port==2] <- 1

tug.cnt <- rep(0,36739)
for(i in 1:36739){
  if(!is.na(pilot$tug3[i])) {
    tug.cnt[i] = tug.cnt[i]+1
  }
}

wt.lv <- matrix(rep(0,36251*8),ncol = 8)
for(i in 1:length(newdf$weight)) {
  if(newdf$weight[i] < 5000) {
    wt.lv[i,1] = 1
  }
  else if(newdf$weight[i] < 10000) {
    wt.lv[i,2] = 1
  }
  else if(newdf$weight[i] < 15000) {
    wt.lv[i,3] = 1
  }
  else if(newdf$weight[i] < 30000) {
    wt.lv[i,4] = 1
  }
  else if(newdf$weight[i] < 45000) {
    wt.lv[i,5] = 1
  }
  else if(newdf$weight[i] < 60000) {
    wt.lv[i,6] = 1
  }
  else if(newdf$weight[i] < 100000) {
    wt.lv[i,7] = 1
  }
  else {
    wt.lv[i,8] = 1
  }
}

mm <- matrix(rep(0,36251*12),ncol = 12)
for(i in 1:36251) {
  mm[i,month[i]] = 1
}