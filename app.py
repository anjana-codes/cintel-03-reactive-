import plotly.express as px
from shiny.express import input, ui
from shinywidgets import render_plotly
from shiny import reactive, render, req
import palmerpenguins
import seaborn as sns
import pandas as pd
import shinyswatch

# Theme
shinyswatch. theme.darkly()

#Use the built-in function to load Palmer Penguins Dataset
penguins_df= palmerpenguins.load_penguins()

# names the page
ui.page_opts(title="Penguins Data - Anjana", fillable=True)

# creates sidebar for user interaction
with ui.sidebar(open="open"):
    
    ui.h2("Sidebar")
    
 # Creates a dropdown input to choose a column 
    ui.input_selectize(
        "selected_attribute",
        "Select Plotly Attribute",
        ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"],
    )

    ui.input_selectize(
        "selected_gender",
       "Select Sex",
        ["male", "female"],
    )
 #create a numeric input for the number of Plotly histogram bins
    ui.input_numeric("plotly_bin_count", "Number of Plotly bins", 45)
    
    #create a slider input for the number of Seaborn bins
    ui.input_slider("seaborn_bin_count", "Number of Seaborn bins", 1, 100, 45)

    
    #create a checkbox group input to filter the species
    ui.input_checkbox_group(
        "selected_species_list",
        "Select Species",
        ["Adelie", 
         "Gentoo", 
         "Chinstrap"],
        selected=["Adelie", "Gentoo", "Chinstrap"],
        inline=False,
    )
    
# Adds a hyperlink to GitHub Repo
    ui.a(
        "Anjana's GitHub",
         href="https://github.com/anjana-codes/cintel-02-data",
         target="_blank",
         )
# create a layout to include 2 cards with a data table and data grid
with ui.accordion(id="acc", open="closed"):
    with ui.accordion_panel("Data Table"):
        @render.data_frame
        def penguin_datatable():
            return render.DataTable( filtered_data())

    with ui.accordion_panel("Data Grid"):
        @render.data_frame
        def penguin_datagrid():
            return render.DataGrid( filtered_data())

#Plotly Histogram
with ui.navset_card_tab(id="tab"):
    with ui.nav_panel("Plotly Histogram"):
         ui.card_header("Plotly Histogram: Species")

         @render_plotly
         def plotly_histogram():
            plotly_hist = px.histogram(
                data_frame= filtered_data(),
                x=input.selected_attribute(),
                nbins=input.plotly_bin_count(),
                color="species",
                color_discrete_map={
                     'Adelie': 'yellow',
                     'Chinstrap': 'brown',
                     'Gentoo': 'green'} 
            ) 
            return plotly_hist
#Seaborn Histogram
    with ui.nav_panel("Seaborn Histogram"):
        ui.card_header("Seaborn Histogram: Species")

        @render.plot
        def seaborn_histogram():
           seaborn_plot = sns.histplot(
                data= filtered_data(),
                x=input.selected_attribute(),
                bins=input.seaborn_bin_count(),
                multiple="dodge",
                hue="species",
                palette={
                     'Adelie': 'yellow',
                     'Chinstrap': 'brown',
                     'Gentoo': 'green'},
            )
          
            
#Plotly Scatterplot      
    with ui.nav_panel("Plotly Scatterplot"):
        ui.card_header("Plotly Scatterplot: Species")

        @render_plotly
        def plotly_scatterplot():
            return px.scatter(
                 filtered_data(),
                x="body_mass_g",
                y="bill_length_mm",
                color="species",
                 color_discrete_map={
                     'Adelie': 'yellow',
                     'Chinstrap': 'brown',
                     'Gentoo': 'green'},
            )



    with ui.nav_menu("Pie Chart"):
        with ui.nav_panel("Pie Chart"):
            species_distribution = penguins_df["species"].value_counts().reset_index()
            species_distribution.columns = ["species", "count"]
            @render_plotly
            def pie_chart():
                return px.pie(
                    species_distribution,
                    values="count",
                    names="species",
                    title="Species Distribution",
                    color="species",
                    color_discrete_map={
                     'Adelie': 'yellow',
                     'Chinstrap': 'brown',
                     'Gentoo': 'green'} 

                )
 # Reactive calculations and effects
    # --------------------------------------------------------

    # Add a reactive calculation to filter the data
    # By decorating the function with @reactive, we can use the function to filter the data
    # The function will be called whenever an input function used to generate that output changes.
    # Any output that depends on the reactive function (e.g., filtered_data()) will be updated when the data changes.


        @reactive.calc
        def filtered_data():
         return penguins_df[penguins_df["species"].isin(input.selected_species_list())]
