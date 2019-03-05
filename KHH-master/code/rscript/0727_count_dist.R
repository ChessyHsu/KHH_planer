pier.cnt <- 131
dist.within2 <- matrix(rep(0,pier.cnt^2),nrow=pier.cnt)

for(i in 1:pier.cnt) {
  for(j in 1:pier.cnt) {
    dist.within2[i,j] = distm(cbind(pier.pt$long[i],pier.pt$lat[i]),cbind(pier.pt$long[j],pier.pt$lat[j]))
  }
}

dist.tr <- rep(0,4969)
for(i in 1:4969) {
     p1 <- as.character(df2$place1[i])
     p2 <- as.character(df2$place2[i])
     for(j in 1:131) {
       if(p1 == rownames(dist.within[j,]))  break
     }
     for(k in 1:131) {
       if(p2 == colnames(dist.within[k])) break
     }
     dist.tr[i] = dist.within[j,k]
}

for(i in 1:36250) {
  if(ddd[i] == -1) {
    pier = strtoi(ppp$place2[i])
    found = FALSE
    for(j in 1:187) {
      if(dist.io$pier[j] == pier) {
        found = TRUE
        break
      }
    }
    if(found) {
      if(df$port[i] == 1 && df$status == 1)
        ddd[i] = dist.io$in1[j]
      else if(df$port[i] == 2 && df$status == 1)
        ddd[i] = dist.io$in2[j]
      else if(df$port[i] == 1 && df$status == 3)
        ddd[i] = dist.io$out1[j]
      else if(df$port[i] == 2 && df$status == 3)
        ddd[i] = dist.io$out2[j]
    }
    else {
      print(pier)
      break
    }
  }
}
