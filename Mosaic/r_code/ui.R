# load GUI package
shinyUI(
  pageWithSidebar(
    headerPanel(""),
    sidebarPanel(
      h3("G6PD Fluorometric Analysis"),
      img(src="PATH_2C.JPG",  height=50, width=100),
      fileInput("file1s", "Import *.FCS Files", multiple=TRUE,  accept=NULL),
      checkboxInput("amplification", "Check if Amplification is Linear (Accuri)", TRUE),
      numericInput("file_idx","Select a file for visualization ", 1, min=1, max=100, step=1),
      selectInput("plottype", "Visualization:", 
                  c("Calculated Bright Cells", "FSC and SSC","FSC and FL1", "SSC and FL1")),
      sliderInput("fsc_filt", "Gate FSC", 0, 1, value=c(.4, .95), .01),
      sliderInput("ssc_filt", "Gate SSC", 0, 1, value=c(.05, .6), .01),
      br(),
      numericInput("fl1", "FL1 Channel:", 9),
      numericInput("fsc", "FSC Channel:", 7),
      numericInput("ssc", "SSC Channel:", 8),
      br(),
      br(),
      downloadButton('downloadData', 'Download Batch Results')
    ),
    mainPanel(
      tabsetPanel(
        tabPanel("Visualizations", h4(textOutput("caption")),
                 plotOutput(outputId="picture", width="100%"),
                 h4(textOutput("tabletitle")), tableOutput("view")), 
        tabPanel("Results Table", h4(textOutput("batchresults")), tableOutput('table'))
      )
    )
  )
)
