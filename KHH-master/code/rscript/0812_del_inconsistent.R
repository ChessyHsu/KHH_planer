del = vector()
i = 1
k = nrow(nndf)
while(i < k) {
  if(nndf$start_time[i]==nndf$start_time[i+1] & nndf$shipID[i]==nndf$shipID[i+1]) {
    j = i
    max = j
    while(nndf$start_time[j]==nndf$start_time[j+1] & nndf$shipID[j]==nndf$shipID[j+1]) {
      if(nndf$work_time[j+1] >= nndf$work_time[max]) {
        max = j+1
        del = append(del, -j)
      }
      else{
        del = append(del, -(j+1))
      }
      j = j+1
    }
    i = j
  }
  i = i+1
}
