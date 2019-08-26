model_table <- function(input, inFile){
  inFile <- input$file1s  
  if (is.null(inFile)){
    return(NULL)
  }
  zygosity <- array(0, dim=c(length(inFile$datapath), 5))
  for (i in 1:length(inFile$datapath)){
    dat <- read.FCS(inFile$datapath[i], transformation=FALSE)
    dat <- exprs(dat)
    dat <- dat[which(dat[, input$fl1] > 0, arr.ind=TRUE), ]
    
    # toggle for linear and log data
    if (input$amplification == FALSE){
      dat <- dat
    }
    else if (input$amplification == TRUE){
      dat[, input$fl1] <-  log10(dat[, input$fl1])
    }
    ecdf.fsc <- ecdf(dat[, input$fsc])
    ecdf.ssc <- ecdf(dat[, input$ssc])
    fsc <- which(ecdf.fsc(dat[, input$fsc]) >= input$fsc_filt[1] & ecdf.fsc(dat[, input$fsc]) <= input$fsc_filt[2], arr.ind=FALSE)
    ssc <- which(ecdf.ssc(dat[, input$ssc]) >= input$ssc_filt[1] & ecdf.ssc(dat[, input$ssc]) <= input$ssc_filt[2], arr.ind=FALSE)
    keep <- intersect(fsc, ssc)
    fl1h <- dat[keep, input$fl1]
    
    # mean, median, sd
    meanFITC = round(mean(100*fl1h/max(fl1h)), 1)
    medianFITC = round(median(100*fl1h/max(fl1h)), 1)
    sdFITC = round(sd(100*fl1h/max(fl1h)), 1)
    
    # ks density of fl1 data
    d <- density(fl1h, n=100)
    
    # normalize data for peak intensity = 1
    freq = d$y/sum(d$y)
    intensity = 100*d$x/max(d$x)
    
    # smooth spline
    smoothingSpline = smooth.spline(intensity, freq, spar=0.50)
    
    # find local maxima by executing peaks.r
    loc1 = intensity[which.peaks(smoothingSpline$y, partial=TRUE, decreasing=FALSE)]
    peak1 = freq[which.peaks(smoothingSpline$y, partial=TRUE, decreasing=FALSE)]
    loc2 = loc1[which(peak1 > .003)] # remove very small peaks
    loc3 = loc2[which(loc2 < 99)]
    if (length(which(loc3 > max(loc3) - 10)) == length(loc3)) {
      maxima = max(loc3)
    } else {
      maxima = c(min(loc3), max(loc3))
      meanidx = which(abs(intensity - mean(maxima)) == min(abs(intensity - mean(maxima))))
      meanidx = max(meanidx)
    }
    # % bright cells
    if (length(maxima) == 2){
      np = round(100*sum(freq[meanidx:100]), digits=1)
    } else if (length(maxima) == 1 && maxima > 75){
      A = log(maxima)
      B = A - .15
      D = exp(B)
      E = which(abs(intensity - D) == min(abs(intensity - D)))
      np = round(100*sum(freq[E:100]), digits=1)
    } else if (length(maxima) == 1 && maxima <= 75){
      A = log(maxima)
      B = A + .15
      D = exp(B)
      E = which(abs(intensity - D) == min(abs(intensity - D)))
      np = round(100*sum(freq[E:100]), digits=1)
    }       
    
    # make table
    zygosity[i, 1] = inFile$name[i]
    zygosity[i, 2] = as.character(meanFITC)
    zygosity[i, 3] = as.character(medianFITC)
    zygosity[i, 4] = as.character(sdFITC)
    zygosity[i, 5] = as.character(np) 
  }
  
  zygo.results <- as.table(zygosity)
  colnames(zygo.results) <- c("File Name", "Mean FL1","Median FL1" ,"Std Dev FL1", "% Bright Cells")
  rownames(zygo.results) <- c(1:length(zygosity[, 1]))
  zygo.results
}