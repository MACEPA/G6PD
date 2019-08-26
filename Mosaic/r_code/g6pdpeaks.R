which_peaks <- function(x, partial=TRUE, decreasing=FALSE){
  if (decreasing){
    if (partial){
      which(diff(c(TRUE, diff(x) <= 0, FALSE)) > 0)
    } else {
      which(diff(diff(x) <= 0) > 0)
    }    
  } else {
    if (partial){
      which(diff(c(TRUE, diff(x) >= 0, FALSE)) < 0)
    } else {
      which(diff(diff(x) >= 0) < 0)
    }
  }
}
