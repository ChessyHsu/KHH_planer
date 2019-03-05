tug.cur = `colnames<-`(matrix(rep(-1,27),ncol=27), tug.code)
tug.pri <- data.frame(tug1=rep(NA,36250),tug2=rep(NA,36250),tug3=rep(NA,36250))

for(i in 1:36250) {
  tug.pri[i,1] = tug.cur[1,match(pilot.m$tug1[i], tug.code)]
  if(df$status[i]==3) {
    if(df$port[i]==1) {
      tug.cur[1,match(pilot.m$tug1[i], tug.code)] = 100
    }
    else {
      tug.cur[1,match(pilot.m$tug1[i], tug.code)] = 200
    }
    
  }
  else {
    tug.cur[1,match(pilot.m$tug1[i], tug.code)] = pilot.m$place2[i]
  }
  
  if(!is.na(pilot.m$tug2[i])) {
    tug.pri[i,2] = tug.cur[1,match(pilot.m$tug2[i], tug.code)]
    if(df$status[i]==3) {
      if(df$port[i]==1) {
        tug.cur[1,match(pilot.m$tug2[i], tug.code)] = 100
      }
      else {
        tug.cur[1,match(pilot.m$tug2[i], tug.code)] = 200
      }
    }
    else {
      tug.cur[1,match(pilot.m$tug2[i], tug.code)] = pilot.m$place2[i]
    }
  }
  if(!is.na(pilot.m$tug3[i])) {
    tug.pri[i,3] = tug.cur[1,match(pilot.m$tug3[i], tug.code)]
    if(df$status[i]==3) {
      if(df$port[i]==1) {
        tug.cur[1,match(pilot.m$tug3[i], tug.code)] = 100
      }
      else {
        tug.cur[1,match(pilot.m$tug3[i], tug.code)] = 200
      }
    }
    else {
      tug.cur[1,match(pilot.m$tug3[i], tug.code)] = pilot.m$place2[i]
    }
  }
}

tug.pri.dist <- data.frame(tug1=rep(NA,36250),tug2=rep(NA,36250),tug3=rep(NA,36250))
for(i in 1:36250) {
  if(tug.pri[i,1]==-1) {
    tug.pri.dist[i,1] = 0
  }
  else {
    if(df$status[i]==1) {
      if(df$port[i]==1) { # coming via port 1
        if(tug.pri[i,1]==100) {
          tug.pri.dist[i,1] = in1.out1
        }
        else if(tug.pri[i,1]==200) {
          tug.pri.dist[i,1] = in1.out2
        }
        else {
          pier.index = match(tug.pri[i,1], dist.io$pier)
          if(!is.na(pier.index))  tug.pri.dist[i,1] = dist.io$in1[pier.index]
          else tug.pri.dist[i,1] = -1
        }
      }
      else if(df$port[i]==2) { # inport via port 2
        if(tug.pri[i,1]==100) {
          tug.pri.dist[i,1] = in2.out1
        }
        else if(tug.pri[i,1]==200) {
          tug.pri.dist[i,1] = in2.out2
        }
        else {
          pier.index = match(tug.pri[i,1], dist.io$pier)
          if(!is.na(pier.index))  tug.pri.dist[i,1] = dist.io$in1[pier.index]
          else tug.pri.dist[i,1] = -1
        }
      }
    }
    
    # outport and trandfer
    else {
      pier.index = match(place2[i], dist.io$pier)
      if(!is.na(pier.index)) {
        if(tug.pri[i,1]==100) {
          tug.pri.dist[i,1] =  dist.io$out1[pier.index]
        }
        else if(tug.pri[i,1]==200) {
          tug.pri.dist[i,1] = dist.io$out2[pier.index]
        }
        else {
          p1 = match(place2[i], pier.tr.code)
          p2 = match(tug.pri[i,1], pier.tr.code)
          if(!is.na(p1) & !is.na(p2))
            tug.pri.dist[i,1] = dist.within[p1, p2]
          else
            tug.pri.dist[i,1] = -1
        }
      }
      else
        tug.pri.dist[i,1] = -1
    }
  }
  
  if(!is.na(tug.pri[i,2])) {
    if(tug.pri[i,2] == -1) 
      tug.pri.dist[i,2] = 0
    else {
      if(df$status[i]==1) {
        if(df$port[i]==1) { # coming via port 1
          if(tug.pri[i,2]==100) {
            tug.pri.dist[i,2] = in1.out1
          }
          else if(tug.pri[i,2]==200) {
            tug.pri.dist[i,2] = in1.out2
          }
          else {
            pier.index = match(tug.pri[i,2], dist.io$pier)
            if(!is.na(pier.index))  tug.pri.dist[i,2] = dist.io$in1[pier.index]
            else tug.pri.dist[i,2] = -1
          }
        }
        else if(df$port[i]==2) { # inport via port 2
          if(tug.pri[i,2]==100) {
            tug.pri.dist[i,2] = in2.out1
          }
          else if(tug.pri[i,2]==200) {
            tug.pri.dist[i,2] = in2.out2
          }
          else {
            pier.index = match(tug.pri[i,2], dist.io$pier)
            if(!is.na(pier.index))  tug.pri.dist[i,2] = dist.io$in1[pier.index]
            else tug.pri.dist[i,2] = -1
          }
        }
      }
      
      # outport and trandfer
      else {
        pier.index = match(place2[i], dist.io$pier)
        if(!is.na(pier.index)) {
          if(tug.pri[i,2]==100) {
            tug.pri.dist[i,2] =  dist.io$out1[pier.index]
          }
          else if(tug.pri[i,2]==200) {
            tug.pri.dist[i,2] = dist.io$out2[pier.index]
          }
          else {
            p1 = match(place2[i], pier.tr.code)
            p2 = match(tug.pri[i,2], pier.tr.code)
            if(!is.na(p1) & !is.na(p2))
              tug.pri.dist[i,2] = dist.within[p1, p2]
            else
              tug.pri.dist[i,2] = -1
          }
        }
        else
          tug.pri.dist[i,1] = -1
      }
    }
    
    
    if(!is.na(tug.pri[i,3])) {
      if(tug.pri[i,3]==-1) {
        tug.pri.dist[i,3] = 0
      }
      else {
        if(df$status[i]==1) {
          if(df$port[i]==1) { # coming via port 1
            if(tug.pri[i,3]==100) {
              tug.pri.dist[i,3] = in1.out1
            }
            else if(tug.pri[i,3]==200) {
              tug.pri.dist[i,3] = in1.out2
            }
            else {
              pier.index = match(tug.pri[i,3], dist.io$pier)
              if(!is.na(pier.index))  tug.pri.dist[i,3] = dist.io$in1[pier.index]
              else tug.pri.dist[i,3] = -1
            }
          }
          else if(df$port[i]==2) { # inport via port 2
            if(tug.pri[i,3]==100) {
              tug.pri.dist[i,3] = in2.out1
            }
            else if(tug.pri[i,3]==200) {
              tug.pri.dist[i,3] = in2.out2
            }
            else {
              pier.index = match(tug.pri[i,3], dist.io$pier)
              if(!is.na(pier.index))  tug.pri.dist[i,3] = dist.io$in1[pier.index]
              else tug.pri.dist[i,3] = -1
            }
          }
        }
        
        # outport and trandfer
        else {
          pier.index = match(place2[i], dist.io$pier)
          if(!is.na(pier.index)) {
            if(tug.pri[i,3]==100) {
              tug.pri.dist[i,3] =  dist.io$out1[pier.index]
            }
            else if(tug.pri[i,3]==200) {
              tug.pri.dist[i,3] = dist.io$out2[pier.index]
            }
            else {
              p1 = match(place2[i], pier.tr.code)
              p2 = match(tug.pri[i,3], pier.tr.code)
              if(!is.na(p1) & !is.na(p2))
                tug.pri.dist[i,3] = dist.within[p1, p2]
              else
                tug.pri.dist[i,3] = -1
            }
          }
          else
            tug.pri.dist[i,1] = -1
        }
      }
    }
  }
}
