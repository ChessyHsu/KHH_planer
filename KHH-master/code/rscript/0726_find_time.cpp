#include <Rcpp.h>
using namespace Rcpp;

// This is a simple example of exporting a C++ function to R. You can
// source this function into an R session using the Rcpp::sourceCpp 
// function (or via the Source button on the editor toolbar). Learn
// more about Rcpp at:
//
//   http://www.rcpp.org/
//   http://adv-r.had.co.nz/Rcpp.html
//   http://gallery.rcpp.org/
//

// [[Rcpp::export]]
NumericVector timesTwo(NumericVector x) {
  return x * 2;
}

// [[Rcpp::export]]
NumericVector patch_time(NumericVector t, NumericVector num1, NumericVector date1, NumericVector io1, NumericVector num2, NumericVector date2, NumericVector io2) {
  NumericVector time (num1.length());
  time.fill(-1);
  for(int i=0; i<num1.length(); i++) {
    for(int j=0; j<num2.length(); j++) {
      if(num1[i]==num2[j] && date1[i]==date2[j] && io1[i]==io2[j]) {
        time[i] = t[j];
        break;
      }
    }
    
  }
  return time;
}

// [[Rcpp::export]]
NumericVector patch_worktime(NumericVector t, NumericVector num1, NumericVector date1, NumericVector io1, NumericVector num2, NumericVector date2, NumericVector io2) {
  NumericVector worktime (num1.length());
  worktime.fill(-1);
  for(int i=0; i<num1.length(); i++) {
    for(int j=0; j<num2.length(); j++) {
      if(num1[i]==num2[j] && date1[i]==date2[j] && io1[i]==io2[j]) {
        worktime[i] = t[j];
        break;
      }
    }
  }
  return worktime;
}
// [[Rcpp::export]]
NumericVector patch_dist(NumericVector status, NumericVector place, NumericVector port, NumericVector pier, NumericVector inport1, NumericVector inport2, NumericVector outport1, NumericVector outport2) {
  NumericVector dist (status.length());
  dist.fill(-1);
  for(int i=0; i<status.length(); i++) {
    if(status[i] == 1) {
      for(int j=0; j<pier.length(); j++) {
        if(place[i] == pier[j]){
          if(port[i] == 1) {
            dist[i] = inport1[j];
          }
          else if(port[i] == 2) {
            dist[i] = inport2[j];
          }
        }
      }
    }
    else if(status[i] == 3) {
      for(int j=0; j<pier.length(); j++) {
        if(place[i] == pier[j]){
          if(port[i] == 1) {
            dist[i] = outport1[j];
          }
          else if(port[i] == 2) {
            dist[i] = outport2[j];
          }
        }
      }
    }
  }
  return dist;
}

// [[Rcpp::export]]
NumericVector wind_power(NumericVector port, NumericVector port1_power, NumericVector port2_power, NumericVector date1, NumericVector time1, NumericVector date2, NumericVector time2) {
  NumericVector power (date1.length());
  power.fill(-1);
  for(int i=0; i<date1.length(); i++) {
    for(int j=0; j<date2.length(); j++) {
      if(date1[i] == date2[j] && time1[i] == time2[j]){
        if(port[i] == 2) {
          power[i] = port2_power[j];
          break;
        }
        else {
          power[i] = port1_power[j];
          break;
        }
      }
    }
  }
  return power;
}


// You can include R code blocks in C++ files processed with sourceCpp
// (useful for testing and development). The R code will be automatically 
// run after the compilation.
//

/*** R

*/
