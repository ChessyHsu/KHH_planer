ac_tug = rep(0,length(codesum))
type = c(143,145,151,152,153,155,112,241,245,321,322,101,302,104,106,108,109,303,306,308,301,161,162,163,165,401,451,171,172,181,182)
j = 1
for(i in codesum){
  m = match(i, type)
  if(!is.na(m)) {
    if(m <= 2) ac_tug[j] = 117
    else if(m <= 9) ac_tug[j] = 118
    else if(m <= 17) ac_tug[j] = 119
    else if(m <= 23) ac_tug[j] = 120
    else ac_tug[j] = 130
  }
  j = j+1
}

i = 1
k = nrow(n3df)
ignore = 0
greater = vector()
less = vector()
while(i <= k){
  if(n3df$tug_type[i] == 0) {
    ignore = ignore+1
  }
  else if(n3df$tug_cnt[i] == 1) {
    if(n3df$weight_lv[i] == 1) {
      if(n3df$tug_type[i] > 117)  greater = append(greater, i)
    }
    else if(n3df$weight_lv[i] <= 3) {
      if(n3df$tug_type[i] > 118)  greater = append(greater, i)
      else if(n3df$tug_type[i] < 118) less = append(less, i)
    }
    else if(n3df$weight_lv[i] <= 5) {
      if(n3df$tug_type[i] > 119)  greater = append(greater, i)
      else if(n3df$tug_type[i] < 119) less = append(less, i)
    }
    else if(n3df$weight_lv[i] == 6) {
      if(n3df$tug_type[i] > 120)  greater = append(greater, i)
      else if(n3df$tug_type[i] < 120) less = append(less, i)
    }
    else {
      if(n3df$tug_type[i] < 130) less = append(less, i)
    }
  }
  else if(n3df$tug_cnt[i] == 2) {
    if(n3df$shipID[i] == n3df$shipID[i+1]) {
      if(n3df$weight_lv[i] <= 2) {
        if(n3df$tug_type[i] > 117) greater = append(greater, i)
        if(n3df$tug_type[i+1] > 117) greater = append(greater, i)
      }
      else if(n3df$weight_lv[i] <= 3) {
        if(n3df$tug_type[i] == 118) {
          greater = append(greater, i+1)
        }
        else {
          if(n3df$tug_type[i] > 117) greater = append(greater, i)
          else if (n3df$tug_type[i] < 117) less = append(less, i)
          if(n3df$tug_type[i+1] > 118) greater = append(greater, i+1)
          else if (n3df$tug_type[i+1] < 118) less = append(less, i+1)
        }
      }
      else if(n3df$weight_lv[i] <= 4) {
        if(n3df$tug_type[i] == 119) {
          greater = append(greater, i+1)
        }
        else {
          if(n3df$tug_type[i] > 118) greater = append(greater, i)
          else if (n3df$tug_type[i] < 118) less = append(less, i)
          if(n3df$tug_type[i+1] > 119) greater = append(greater, i+1)
          else if (n3df$tug_type[i+1] < 119) less = append(less, i+1)
        }
      }
      else if(n3df$weight_lv[i] <= 5) {
        if(n3df$tug_type[i] > 119) greater = append(greater, i)
        else if (n3df$tug_type[i] < 119) less = append(less, i)
        if(n3df$tug_type[i+1] > 119) greater = append(greater, i+1)
        else if (n3df$tug_type[i+1] < 119) less = append(less, i+1)
      }
      else if(n3df$weight_lv[i] <= 6) {
        if(n3df$tug_type[i] > 120) greater = append(greater, i)
        else if (n3df$tug_type[i] < 120) less = append(less, i)
        if(n3df$tug_type[i+1] > 120) greater = append(greater, i+1)
        else if (n3df$tug_type[i+1] < 120) less = append(less, i+1)
      }
      else if(n3df$weight_lv[i] <= 7) {
        if(n3df$tug_type[i] > 130) greater = append(greater, i)
        else if (n3df$tug_type[i] < 130) less = append(less, i)
        if(n3df$tug_type[i+1] > 130) greater = append(greater, i+1)
        else if (n3df$tug_type[i+1] < 130) less = append(less, i+1)
      }
      else {
        if(n3df$tug_type[i] > 130) greater = append(greater, i)
        else if (n3df$tug_type[i] < 130) less = append(less, i)
        if(n3df$tug_type[i+1] > 130) greater = append(greater, i+1)
        else if (n3df$tug_type[i+1] < 130) less = append(less, i+1)
      }
      i = i+1
    }
    else {
      ignore = ignore+1
    }
  }
  else if(n3df$tug_cnt[i] == 3) {
    ignore = ignore+1
  }
  i = i+1
}
cat('greater: ',length(greater) / (nrow(n3df)-ignore))
cat('smaller: ',length(less) / (nrow(n3df)-ignore))