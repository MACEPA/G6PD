# load GUI package
library("shiny")
library("flowCore")
source("g6pdpeaks.R")
source("model_caption.R")
source("model_table.R")
source("calcbrightcells.R")

shinyServer(function(input, output) {
	formulaText <- reactive({
		paste(input$plottype)
	})

	inFilem <- reactive({
		paste(input$file1m)
	})

	# Return the formula text for printing as a caption
	output$caption <- renderText({
		inFile <- input$file1s  
		if (is.null(inFile)){
			return(NULL)
		}
		if (formulaText() == "Calculated Bright Cells"){
			model_caption(input, inFile) 
		} else {
			paste(inFile$name[input$file_idx], " ~ FSC vs SSC")
		}
	})

	output$tabletitle <- renderText({
		inFile <- input$file1s  
		if (is.null(inFile)){
			return(NULL)
		}
		"Cytometry Channels"
	})

	output$batchresults <- renderText({
		inFile <- input$file1s  
		if (is.null(inFile)){
			return(NULL)
		}
		"Results"
	})


	#########################################data table############################################  
	output$view <- renderTable({
		inFile <- input$file1s  
		if (is.null(inFile)){
			return(NULL)
		}
		dat <- read.FCS(inFile$datapath[1], which.lines=1, transformation=FALSE)
		dat <- exprs(dat)
		dat[1, ] <- 1:length(dat[1, ])
		dat <- round(dat[1, ], digits=0)
		dat <- data.frame(dat)
		dat <- t(dat)
		rownames(dat) <- "channel"
		head(dat, n=1)
	}) 


	###############################BATCH TABLE########################################################  
	datasetInput <- reactive({
		model_table(input,inFile)
	})

	output$table <- renderTable({
		datasetInput()
	})

	output$downloadData <- downloadHandler(
		filename = function(){paste("G6PD_results", '.csv', sep='')},
		content = function(file) {
		  write.csv(datasetInput(), file)
		}
	)


	########################################visualiztions#####################################
	output$picture <- renderPlot({
		inFile <- input$file1s  
		if (is.null(inFile)){
		  return(NULL)
		}

		# data import
		dat <- read.FCS(inFile$datapath[input$file_idx], transformation=FALSE)
		dat <- exprs(dat)

		# remove zero elements
		dat<- dat[which(dat[, input$fl1] > 0, arr.ind=TRUE), ]

		# toggle for linear and log data
		if (input$amplification == FALSE){
			dat <- dat
		} else if (input$amplification == TRUE){
			dat[, input$fl1] <- log10(dat[, input$fl1])
		}

		# prep data
		ecdf.fsc <- ecdf(dat[, input$fsc])
		ecdf.ssc <- ecdf(dat[, input$ssc])
		fsc <- which(ecdf.fsc(dat[, input$fsc]) >= input$fsc_filt[1] & ecdf.fsc(dat[, input$fsc]) <= input$fsc_filt[2], arr.ind=FALSE)
		ssc <- which(ecdf.ssc(dat[, input$ssc]) >= input$ssc_filt[1] & ecdf.ssc(dat[, input$ssc]) <= input$ssc_filt[2], arr.ind=FALSE)
		keep <- intersect(fsc, ssc)

		#plot
		if (input$plottype =="FSC and SSC"){
			datfsc <- dat[keep, input$fsc]
			datssc <- dat[keep, input$ssc]
			splot <- t(rbind(datfsc, datssc))
			plot(splot[, 2], splot[, 1], xlab="Side Scatter", ylab="Forward Scatter")
		} else if (input$plottype == "FSC and FL1"){
			datfsc <- dat[keep, input$fsc]
			datfl1 <- dat[keep, input$fl1]
			splot <- t(rbind(datfsc, datfl1))
			plot(splot[, 1], splot[, 2], xlab="Forward Scatter", ylab="Fl1 Channel")
		} else if (input$plottype =="SSC and FL1"){
			datssc <- dat[keep, input$ssc]
			datfl1 <- dat[keep, input$fl1]
			splot <- t(rbind(datssc, datfl1))
			plot(splot[, 1], splot[, 2],xlab="Side Scatter", ylab="Fl1 Channel", nbin=200)
		} else if (input$plottype =="Calculated Bright Cells"){
			calc_bright_cells(input, inFile)
		}
	})
})



  