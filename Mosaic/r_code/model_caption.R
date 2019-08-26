model_caption<-function(input, inFile){
  inFile <- input$file1s  
  if (is.null(inFile)){
    return(NULL) 
  }
  # data import
  dat <- read.FCS(inFile$datapath[input$file_idx], transformation=FALSE)
  paste(inFile$name[input$file_idx], " ~ G6PD Activity")
} 
