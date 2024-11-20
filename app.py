

from shiny import App, Inputs, Outputs, Session, ui, render, reactive
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd  # Import pandas here
from shinywidgets import output_widget, render_widget
import shinyswatch
from palmerpenguins import load_penguins 
import seaborn as sns
import ipyleaflet as ipyl
from shinywidgets import render_plotly
from pathlib import Path  

# Load the Palmer Penguins dataset
penguins_df = load_penguins()
penguins_df.head()




# Define UI
app_ui = ui.page_fluid(
    ui.row(
        # Column for the image (set to 4/12 of the row width)
        ui.column(2,  # Column for the image (takes up 2/12 of the row)
            ui.div(
                ui.output_image("image", height="100px"),  # Image output
                style="border: 1px solid #ccc; padding: 0px; margin: 1px; border-radius: 0.75px; max-width: 30%; height:80px; object-fit: contain;"
            )
        ),
        
        # Column for the heading (Penguin Dashboard)
        ui.column(10,  # Column for the heading (takes up 10/12 of the row)
            ui.h2("Penguin Dashboard", 
                style="background-color:orange; color:Blue; text-align: center; padding: 10px; margin: auto; border-radius: 5px;"
            )
        )
    ),
    
    ui.row(
        ui.column(4, 
            ui.div(
                ui.output_plot("bar_chart", height="350px"),  # histogram output
                style="border: 1px solid #ccc; padding: 10px; margin: 10px; border-radius: 5px;"
            )
        ),
        ui.column(4, 
            ui.div(
                output_widget("plot1", height="350px"),  # Set height for plot1
                style="border: 1px solid #ccc; padding: 10px; margin: 10px; border-radius: 5px;"
            )
        ),
        ui.column(4, 
            ui.div(
                output_widget("density_plot", height="350px"),  # Set height for density plot
                style="border: 1px solid #ccc; padding: 10px; margin: 10px; border-radius: 5px;"
            )
        )
    ),
    ui.row(
        ui.column(4, 
            ui.div(
                output_widget("scatter_plot", height="500px"),  # Set height for scatter plot
                style="border: 1px solid #ccc; padding: 10px; margin: 10px; border-radius: 5px;"
            )
        ),
        ui.column(8,  # Wider column for the inputs
            ui.div(
                ui.row(
                    ui.column(3, 
                        ui.input_checkbox_group(
                            "selected_species_list", 
                            "Choose Species", 
                            ["Adelie", "Gentoo", "Chinstrap"], 
                            selected=["Adelie"], 
                            inline=True  # Display inline
                        )
                    ),
                    ui.column(3, 
                        ui.input_checkbox_group(
                            "selected_island_list", 
                            "Choose Island", 
                            ["Biscoe", "Dream", "Torgersen"], 
                            selected=["Biscoe"], 
                            inline=True  # Display inline
                        )
                    ),
                    ui.column(3, 
                        ui.input_selectize(
                            "sex", 
                            "Select Sex:", 
                            {"male": "male", "female": "female"}, 
                            multiple=True, 
                            selected=['female']
                        )
                    ),
                    ui.column(3, 
                        ui.input_selectize(
                            "selected_attribute", 
                            "Penguin Metric",  
                            ["bill_length_mm", "bill_depth_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"]
                        )
                    ),
                    ui.column(2, 
                        ui.input_numeric(
                            "n", 
                            "Number of Bins", 
                            value=10, 
                            min=1, 
                            max=20
                        )
                    )
                )
            )
        )
    ),
    ui.row(
        ui.column(12, 
            ui.div(
                ui.output_table("data_table", style="overflow: auto; height: 350px;"),  # Set height for data table
                style="border: 1px solid #ccc; padding: 10px; margin: 10px; border-radius: 5px;"
            )
        )
    )
)
 

def server(input, output, session):   
    @reactive.calc
    def filtered_df():          
        selected_species = input.selected_species_list()
        selected_island = input.selected_island_list()
        selected_sex = input.sex()
        filtered = penguins_df[penguins_df["species"].isin(selected_species) & penguins_df["island"].isin(selected_island)
                               & penguins_df["sex"].isin(selected_sex)]
        return filtered

    @output
    @render.image  
    def image():
        here = Path(__file__).parent
        img_path = "C:/Users/Mahi2/Pictures/shiny1.png"  
        img = {"src": img_path, "width": "80px"} 
        return img
        
    @output
    @render.table
    def data_table():
          #return render.DataTable(filtered_df(), selection_mode="row")
          return filtered_df()

  
    @output
    @render.table
    def filtered_table():
          return filtered_df()
        
    @output
    @render.plot
    def bar_chart():
            df = filtered_df() 
            plt.figure(figsize=(6,4))  # Set the figure size
            sns.histplot(data=df, x="species",  hue="species", multiple="stack", kde=False, palette="Set2", discrete=True)
            plt.title("Unique Penguin Species Count by Island and Gender")
            plt.xlabel("Species")
            plt.ylabel("Count")
            return plt.gcf()  # Return the current figure
    
   
    @output
    @render_widget
    def plot1(): 
        df = filtered_df()
        n_bins = input.n()  
        fig = px.histogram(df, x=input.selected_attribute(), color="species", 
                           title="Distribution of Species by attribute", 
                           barmode='group', 
                           color_discrete_sequence=px.colors.qualitative.Set2,  nbins=n_bins)
        fig.update_layout(bargap=0.2)  # Set bar gap
        return fig


    @output
    @render_widget
    def density_plot(): 
        df = filtered_df()
         # Calculate the number of unique species for selected islands
        selected_attribute = input.selected_attribute()
        fig = px.density_contour(df, x=selected_attribute, 
            color="species",
            histnorm='density',  # Normalize the histogram for density
            title=f"Density Histogram of {selected_attribute.replace('_', ' ').title()} by Species",
            color_discrete_sequence=px.colors.qualitative.Set2 )
        fig.update_traces(
        line=dict(width=2)  # Set the width of the contour lines
    )
        
         # Update the traces to fill contours and set transparency
        fig.update_layout( 
            title_font=dict(size=18),  # Increase title font size
            xaxis_title=dict(font=dict(size=14)),  # X-axis title font size
            yaxis_title=dict(font=dict(size=14)),  # Y-axis title font size
            legend_title=dict(font=dict(size=14)),  # Legend title font size
            legend=dict(font=dict(size=12)),  # Legend font size
            xaxis=dict(showgrid=True, gridcolor='LightGray'),  # Show grid on x-axis
            yaxis=dict(showgrid=True, gridcolor='LightGray'),  # Show grid on y-axis
            plot_bgcolor='rgba(255, 255, 255, 0.5)',  # Set plot background color
            paper_bgcolor='rgba(255, 255, 255, 1)',)  # Set paper background color)  # Set bar gap
        return fig

    @output
    @render_widget
    def scatter_plot():
            df = filtered_df() 
            fig = px.scatter(df,
            x="body_mass_g",
            y="flipper_length_mm",
            color="species", 
            title="Scatter Plot of Body mass vs. Flipper Length",
            labels={"body_mass_g": "Body Mass",
                "flipper_length_mm": "Flipper Length"}
                            )

            
            return fig      
            
   
      
app = App(app_ui, server)


if __name__ == "__main__":
    app.run()
