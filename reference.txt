from shiny.express import input, ui, render
from shinywidgets import render_plotly
import plotly.express as px
from palmerpenguins import load_penguins
from shiny import reactive
import seaborn as sns
import matplotlib.pyplot as plt
import base64
from io import BytesIO


penguins_df = load_penguins()

@reactive.calc
def filtered_data():
    selected_species = input.Selected_Species_List()
    min_mass, max_mass = input.body_mass_range()
    
    
    filtered_df = penguins_df[
        (penguins_df["species"].isin(selected_species)) &
        (penguins_df["body_mass_g"] >= min_mass) &
        (penguins_df["body_mass_g"] <= max_mass)
    ]
    return filtered_df


with ui.sidebar(open="open"):
    ui.h2("Sidebar")
    
    ui.input_selectize(
        "selected_attribute",
        "Penguin Metric",
        ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"],
    )
    ui.input_numeric("plotly_bin_count", "Number of Bins", 50)
    ui.input_slider("seaborn_bin_count", "Seaborn Bins", 1, 50, 20)
    
    ui.input_checkbox_group(
        "Selected_Species_List",
        "Species Selection",
        ["Adelie", "Gentoo", "Chinstrap"],
        selected=["Adelie", "Gentoo", "Chinstrap"],
        inline=False,
    )
    ui.input_slider(
        "body_mass_range",
        "Body Mass Range (g)",
        min=penguins_df["body_mass_g"].min(),
        max=penguins_df["body_mass_g"].max(),
        value=(penguins_df["body_mass_g"].min(), penguins_df["body_mass_g"].max())
    )
    
    ui.input_selectize(
        "scatter_x_axis",
        "Scatter Plot X-Axis",
        ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"],
        selected="body_mass_g"
    )
    ui.input_selectize(
        "scatter_y_axis",
        "Scatter Plot Y-Axis",
        ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"],
        selected="flipper_length_mm"
    )

    ui.hr()
    ui.a(
        "Github",
        href="https://github.com/Queensdelight/cintel-03-reactive/edit/main/app.py",
        target="_blank",
    )

with ui.layout_columns():
   
    with ui.card(full_screen=True):
        @render_plotly
        def plot1():
            filtered_df = filtered_data()
            fig = px.histogram(
                filtered_df,
                x="bill_length_mm",
                title="Histogram of Bill Length",
                color_discrete_sequence=["orange"]
            )
            fig.update_traces(marker_line_color="black", marker_line_width=2)
            return fig


    with ui.card(full_screen=True):
        @render_plotly
        def plot2():
            selected_attribute = input.selected_attribute()
            bin_count = input.plotly_bin_count()
            filtered_df = filtered_data()
            fig = px.histogram(
                filtered_df,
                x=selected_attribute,
                nbins=bin_count,
                title=f"Histogram of {selected_attribute.replace('_', ' ').title()}",
                color_discrete_sequence=["black"]
            )
            fig.update_traces(marker_line_color="white", marker_line_width=2)
            return fig


with ui.layout_columns():
    with ui.card(full_screen=True):
        ui.card_header("Plotly Scatterplot: Custom Axes")

        @render_plotly
        def scatter_plot():
            filtered_df = filtered_data()
            x_axis = input.scatter_x_axis()
            y_axis = input.scatter_y_axis()
            fig = px.scatter(
                filtered_df,
                x=x_axis,
                y=y_axis,
                color="species",
                title=f"Scatter Plot: {x_axis.replace('_', ' ').title()} vs {y_axis.replace('_', ' ').title()}",
                labels={x_axis: x_axis.replace('_', ' ').title(), y_axis: y_axis.replace('_', ' ').title()}
            )
            return fig


    with ui.card(full_screen=True):
        @render_plotly
        def density_plot():
            filtered_df = filtered_data()
            fig = px.density_contour(
                filtered_df,
                x="bill_length_mm",
                y="flipper_length_mm",
                color="species",
                title="Density Plot: Bill Length vs Flipper Length by Species",
                labels={"bill_length_mm": "Bill Length (mm)", "flipper_length_mm": "Flipper Length (mm)"}
            )
            return fig


with ui.layout_columns():
    with ui.card(full_screen=True):
        @render.data_frame
        def data_table():
            return render.DataTable(filtered_data(), selection_mode="row")

    with ui.card(full_screen=True):
        @render.data_frame
        def data_grid():
            return render.DataGrid(filtered_data(), selection_mode="row")


with ui.layout_columns():
    with ui.card(full_screen=True):
        @render.plot(alt="Seaborn histogram of selected penguin metric.")
        def seaborn_histogram():
            selected_attribute = input.selected_attribute()
            bin_count = input.seaborn_bin_count()
            filtered_df = filtered_data()
            histplot = sns.histplot(
                filtered_df[selected_attribute].dropna(), bins=bin_count, kde=True
            )
            histplot.set_title(f"Seaborn Histogram of {selected_attribute.replace('_', ' ').title()}")
            histplot.set_xlabel(selected_attribute.replace('_', ' ').title())
            histplot.set_ylabel("Count")
            return histplot
