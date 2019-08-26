calc_bright_cells <- function(input, inFile){
  # checking for broken input
	inFile <- input$file1s  
	if (is.null(inFile)) {
	  return(NULL)
	}

	# data import
	dat <- read.FCS(inFile$datapath[input$file_idx], transformation=FALSE)
	dat <- exprs(dat)

	# remove zero elements
	# subset to data where FL1 is greater than 0
	dat <- dat[which(dat[, input$fl1] > 0, arr.ind=TRUE), ]

	# toggle for linear and log data
	# if "amplification", change FL1 to log space
	if (input$amplification == TRUE){
		dat[, input$fl1] <-  log10(dat[, input$fl1])
	}

	# run model
	# run "empirical cumulative distribution function" on FSC and SSC
	ecdf.fsc <- ecdf(dat[, input$fsc])
	ecdf.ssc <- ecdf(dat[, input$ssc])
	# keep FSC/SSC data where data is between FSC/SSC lower bound
	# and upper bound filters
	fsc <- which(ecdf.fsc(dat[, input$fsc]) >= input$fsc_filt[1] & 
					ecdf.fsc(dat[, input$fsc]) <= input$fsc_filt[2], arr.ind=FALSE)
	ssc <- which(ecdf.ssc(dat[, input$ssc]) >= input$ssc_filt[1] &
					ecdf.ssc(dat[, input$ssc]) <= input$ssc_filt[2], arr.ind=FALSE)
	keep <- intersect(fsc, ssc)
	fl1h <- dat[keep, input$fl1]

	# age adustment

	# ks density of fl1 data
	d <- density(fl1h, n=100)

	# normalize data for peak (maximum??) intensity = 1
	freq <- d$y/sum(d$y)
	intensity <- 100*d$x/max(d$x)

	# smooth spline
	smoothingSpline <- smooth.spline(intensity, freq, spar=0.50)

	# find local maxima by executing peaks.r
	peak_data <- which_peaks(smoothingSpline$y, partial=TRUE, decreasing=FALSE)
	loc1 <- intensity[peak_data]
	peak1 <- freq[peak_data]
	loc2 <- loc1[which(peak1 > .003)] # remove very small peaks
	loc3 <- loc2[which(loc2 < 99)]

  # Conditions for maxima
	len_condition <- length(which(loc3 > max(loc3) - 10))
	if (len_condition == length(loc3)) {
		maxima <- max(loc3)
	} else {
	  maxima = c(min(loc3), max(loc3))
	  abs_condition = abs(intensity - mean(maxima))
	  meanidx = which(abs_condition == min(abs_condition))
	  meanidx = max(meanidx)
	}

	# percentage of bright cells
	if (length(maxima) == 2){
		np <- round(100*sum(freq[meanidx:100]), digits=1)
	} else if (length(maxima) == 1 && maxima > 75){
		A <- exp(log(maxima) - .15)
		B <- which(abs(intensity - A) == min(abs(intensity - A)))
		np <- round(100*sum(freq[B:100]), digits=1)
	} else if (length(maxima) == 1 && maxima <= 75){
		A <- exp(log(maxima) + .15)
		B <- which(abs(intensity - A) == min(abs(intensity - A)))
		np <- round(100*sum(freq[B:100]), digits=1)
	}

	# call cut offs
	if (length(maxima) > 1){
		mainp <- paste(round(min(loc3), digits=1), round(max(loc3), digits=1),
		               sep=" ")
	} else {
		mainp <- paste(round(max(loc3), digits=1))
	}

	# Label plots based on number of maxima
	if (length(maxima) == 1){
		paste_var <- paste("Standardized Curve with Local Maxima at ", mainp,
						  "- Percentage Bright Cells", as.character(np), "%", sep=" ")
		plot(intensity, freq, type="l", xlab="Normalized FL1 Channel Intensity",
			 ylab="Percetage Observed", main=paste_var)
		polygon(c(intensity[B], intensity[B:100]), c(min(freq), freq[B:100]),
		        col='blue')  
	} else if (length(maxima) == 2){
		paste_var <- paste("Standardized Curve with Local Maxima at ", mainp,
						   "- Percentage Bright Cells",as.character(np),"%",sep=" ")
		plot(intensity, freq, type="l", xlab="Normalized FL1 Channel Intensity",
			 ylab="Percetage Observed", main=paste_var)
		polygon(c(intensity[meanidx], intensity[meanidx:100]),
		        c(min(freq), freq[meanidx:100]), col='blue')
	}
}
