### IN
nndf1 = nndf[nndf$status==1,]
train1.n = sample(1:nrow(nndf1),ceiling(nrow(nndf1)*0.8))
train1 = nndf1[train1.n,]
left1 = nndf1[-train1.n,]
test1.n = sample(1:nrow(left1),ceiling(nrow(left1)*0.5))
test1 = left1[test1.n,]
valid1 = left1[-test1.n,]

wt1 = factor(train1$weight_lv)
d1 = train1$dist
wd1 = train1$wind
sv1 = train1$seven
day1 = train1$day

pt1 = factor(train1$pilotID)
tc1 = factor(train1$tug_cnt)
p1 = factor(train1$port)

lm1 = lm(train1$work_time~wt1+d1+wd1+sv1+day1+pt1+tc1+p1)
summary(lm1)

# validation
pt1 = factor(valid1$pilotID)
p1 = factor(valid1$port)
tc1 = factor(valid1$tug_cnt)
wt1 = factor(valid1$weight_lv)

x1 = data.frame(
  model.matrix(~wt1)[,-1],
  d1 = valid1$dist,
  wd1 = valid1$wind,
  sv1 = valid1$seven,
  day1 = valid1$daynight,
  model.matrix(~pt1)[,-1],
  model.matrix(~tc1)[,-1],
  model.matrix(~p1)[,-1]
)
colnames(x1)[ncol(x1)] = 'p12'
pre1 = predict(lm1, newdata=x1)
sse1 = sum((pre1-valid1$work_time)^2)
mse1 = sum((pre1-valid1$work_time)^2) / (nrow(valid1)-ncol(x1)-1)

# test
pt1 = factor(test1$pilotID)
p1 = factor(test1$port)
tc1 = factor(test1$tug_cnt)
wt1 = factor(test1$weight_lv)

x1 = data.frame(
  model.matrix(~wt1)[,-1],
  d1 = test1$dist,
  wd1 = test1$wind,
  sv1 = test1$seven,
  day1 = test1$daynight,
  model.matrix(~pt1)[,-1],
  model.matrix(~tc1)[,-1],
  model.matrix(~p1)[,-1]
)
colnames(x1)[ncol(x1)] = 'p12'
pre1 = predict(lm1, newdata=x1)
mae1 = mean(abs(pre1-test1$work_time))
mape1 = sum(abs(pre1-test1$work_time)/test1$work_time) / nrow(test1)


### TRANS
nndf2 = nndf[nndf$status==2,]
train2.n = sample(1:nrow(nndf2),ceiling(nrow(nndf2)*0.8))
train2 = nndf2[train2.n,]
left2 = nndf2[-train2.n,]
test2.n = sample(1:nrow(left2),ceiling(nrow(left2)*0.5))
test2 = left2[test2.n,]
valid2 = left2[-test2.n,]

wt2 = factor(train2$weight_lv)
d2 = train2$dist
wd2 = train2$gust
sv2 = train2$seven
day2 = train2$daynight

pt2 = factor(train2$pilotID)
tc2 = factor(train2$tug_cnt)

lm2 = lm(train2$work_time~wt2+d2+wd2+sv2+day2+pt2+tc2)
summary(lm2)

# validation
pt2 = factor(valid2$pilotID)
tc2 = factor(valid2$tug_cnt)
wt2 = factor(valid2$weight_lv)

x2 = data.frame(
  model.matrix(~wt2)[,-1],
  d2 = valid2$dist,
  wd2 = valid2$wind,
  sv2 = valid2$seven,
  day2 = valid2$daynight,
  model.matrix(~pt2)[,-1],
  model.matrix(~tc2)[,-1]
)
pre2 = predict(lm2, newdata=x2)
sse2 = sum((pre2-valid2$work_time)^2)
mse2 = sum((pre2-valid2$work_time)^2) / (nrow(valid2)-ncol(x2)-1)

# test
pt2 = factor(test2$pilotID)
tc2 = factor(test2$tug_cnt)
wt2 = factor(test2$weight_lv)

x2 = data.frame(
  model.matrix(~wt2)[,-1],
  d2 = test2$dist,
  wd2 = test2$gust,
  sv2 = test2$seven,
  day2 = test2$daynight,
  model.matrix(~pt2)[,-1],
  model.matrix(~tc2)[,-1]
)

pre2 = predict(lm2, newdata=x2)
mae2 = mean(abs(pre2-test2$work_time))
mape2 = mean(abs(pre2-test2$work_time)/test2$work_time)

### OUT
nndf3 = nndf[nndf$status==3,]
train3.n = sample(1:nrow(nndf3),ceiling(nrow(nndf3)*0.8))
train3 = nndf3[train3.n,]
left3 = nndf3[-train3.n,]
test3.n = sample(1:nrow(left3),ceiling(nrow(left3)*0.5))
test3 = left3[test3.n,]
valid3 = left3[-test3.n,]

wt3 = factor(train3$weight_lv)
d3 = train3$dist
wd3 = train3$gust
sv3 = train3$seven
day3 = train3$daynight

pt3 = factor(train3$pilotID)
tc3 = factor(train3$tug_cnt)
p3 = factor(train3$port)

lm3 = lm(train3$work_time~wt3+d3+wd3+sv3+day3+pt3+tc3+p3)
summary(lm3)

# validation
pt3 = factor(valid3$pilotID)
p3 = factor(valid3$port)
tc3 = factor(valid3$tug_cnt)
wt3 = factor(valid3$weight_lv)

x3 = data.frame(
  model.matrix(~wt3)[,-1],
  d3 = valid3$dist,
  wd3 = valid3$wind,
  sv3 = valid3$seven,
  day3 = valid3$daynight,
  model.matrix(~pt3)[,-1],
  model.matrix(~tc3)[,-1],
  model.matrix(~p3)[,-1]
)
colnames(x3)[ncol(x3)] = 'p32'
pre3 = predict(lm3, newdata=x3)
sse3 = sum((pre3-valid3$work_time)^2)
mse3 = sum((pre3-valid3$work_time)^2) / (nrow(valid3)-ncol(x3)-1)

# test
pt3 = factor(test3$pilotID)
p3 = factor(test3$port)
tc3 = factor(test3$tug_cnt)
wt3 = factor(test3$weight_lv)

x3 = data.frame(
  model.matrix(~wt3)[,-1],
  d3 = test3$dist,
  wd3 = test3$gust,
  sv3 = test3$seven,
  day3 = test3$day,
  model.matrix(~pt3)[,-1],
  model.matrix(~tc3)[,-1],
  model.matrix(~p3)[,-1]
)
colnames(x3)[ncol(x3)] = 'p32'
pre3 = predict(lm3, newdata=x3)
mae3 = mean(abs(pre3-test3$work_time))
mape3 = mean((abs(pre3-test3$work_time)/test3$work_time)[test3$work_time>0])
