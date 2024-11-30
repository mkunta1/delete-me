
from faicons import icon_svg
import faicons as fa
import plotly.express as px
from shinywidgets import render_plotly, render_widget, output_widget
import random
from shiny import reactive, render
from datetime import datetime
import pandas as pd
from shiny import reactive, render, req
from shiny.express import input, ui,render
from collections import deque
from scipy import stats

UPDATE_INTERVAL_SECS: int = 10
DEQUE_SIZE: int=10
reactive_value_wrapper = reactive.value(deque(maxlen=DEQUE_SIZE))

#import icons from faicons----------------------------------------------------------------------
ICONS={
    "mars": fa.icon_svg("mars"),
    "venus": fa.icon_svg("venus"),
    "currency-dollar": fa.icon_svg("dollar-sign"),
    "gear": fa.icon_svg("gear")
}

tips = px.data.tips() #call in tipping data

#page title-----------------------------------------------------------------------------------------
ui.page_opts(title="Holiday Tipping Competition", fillable=True)

#create sidebar--------------------------------------------------------------------------------------
with ui.sidebar(open="open"):
    ui.h5("Tip Detail Options")

  
    #Checkbox group to select dining time
    ui.input_checkbox_group("selected_dining_time","Select Dining time",
                      ["Dinner","Lunch"],
                      selected=["Dinner","Lunch"],inline=True)
    #Checkbox group to select gender
    ui.input_checkbox_group("selected_gender","Select Gender",["Male","Female"],
                        selected=["Male","Female"], inline=True)
    #dropdown to select x attribute for scatterplot
    ui.input_selectize("selected_x_attribute","Select X Attribute",
                      ["total_bill","smoker","day","time","size","tip"],selected=["total_bill"])
    #dropdown to select y attribute for scatterplot
    ui.input_selectize("selected_y_attribute","Select Y Attribute",
                      ["total_bill","smoker","day","time","size","tip"],selected=["tip"])
    
    #slider to select bill amount (this one is not interactive with tables or charts) 
    #The Double ended slider was based off of code recommended to me by Phillip Fowler
    ui.input_slider("total_bill_amount","Select Total Bill",min=0.00,max=50.00,value=[3.00,50.00],step=0.01)



with ui.layout_columns(fill=False):#Column section 1--------------------------------------
    with ui.value_box(
        showcase=icon_svg("clock"),
        theme="bg-gradient-blue-purple",height=200):
        "Current Date and Time"

        @render.text
        def display_time():
            """Get the latest reading and return a timestamp string"""
            deque_snapshot, df, latest_dictionary_entry = reactive_tips_combined()
            return f"{latest_dictionary_entry['timestamp']}"
            
    #female live tips per table value box-----------------------------------------------------------------
    with ui.value_box(
        showcase=ICONS["venus"],
        theme="bg-gradient-purple-orange", height=200):
        "GIRLS live tips per table"
        @render.text
        def display_gtip():
            deque_snapshot, df, latest_dictionary_entry = reactive_tips_combined()
            return f"${latest_dictionary_entry['girlamnt']}"
        "Currently leading in totals"

    #Male Live tips per table value box----------------------------------------------------------
    with ui.value_box(
        showcase=icon_svg("mars"),
        theme="bg-gradient-green-blue", height=200):
        "BOYS live tips per table"
        @render.text
        def display_btip():
            deque_snapshot, df, latest_dictionary_entry = reactive_tips_combined()
            return f"${latest_dictionary_entry['boyamnt']}"
        "Up from yesterday"

    
#Columns number 2 with graph and table-----------------------------------------------------------
with ui.layout_columns(fill=False):
    
    #Table of tipping data------------------------------------------
    with ui.card():
        "Tipping Data table"
        @render.data_frame
        def tipping_df():
            return render.DataTable(filtered_tips_and_gender(),selection_mode='row')
    
    #Scatter graph of total bill vs total tip---------------------------
    with ui.card(full_screen=True):
        ui.card_header("Your Tips and Tables")
        @render_plotly
        def plotly_scatterplot():
            return px.scatter(
                data_frame=filtered_gender(),
                x=input.selected_x_attribute(),
                y=input.selected_y_attribute(),
                color="sex",
                color_discrete_sequence=["purple","green"],
                labels={"total_bill": "Total Bill",
                   "tip":"Total Tip"})

#tabbed navigation box---------------------------------------------------
with ui.navset_pill(id="tabbed_graphs"):
    with ui.nav_panel("Girls Trend Chart"):#Female trend chart------------------------------------------------
        @render_plotly
        def display_plot():
        # Fetch from the reactive calc function
            deque_snapshot, df, latest_dictionary_entry = reactive_tips_combined()

            # Ensure the DataFrame is not empty before plotting
            if not df.empty:
                # Convert the 'timestamp' column to datetime for better plotting
                df["timestamp"] = pd.to_datetime(df["timestamp"])

        
            fig = px.scatter(df,
            x="timestamp",
            y="girlamnt",
            title="Recorded Female Tips with Regression Line",
            labels={"timestamp": "Time", "girlamnt": "Tips"},
            color_discrete_sequence=["orange"] )
            
          

            # For x let's generate a sequence of integers from 0 to len(df)
            sequence = range(len(df))
            x_vals = list(sequence)
            y_vals = df["girlamnt"]

            slope, intercept, r_value, p_value, std_err = stats.linregress(x_vals, y_vals)
            df['best_fit_line'] = [slope * x + intercept for x in x_vals]

            # Add the regression line to the figure
            fig.add_scatter(x=df["timestamp"], y=df['best_fit_line'], mode='lines', name='Regression Line')

            #update layout as neeted to customize further
            fig.update_layout(xaxis_title="Time", yaxis_title="Tip Amount $")
            fig.update_layout(height=300)
    
            return fig
            
    with ui.nav_panel("Boys Trend Chart"):#male trend chart------------------------------------------------
        @render_plotly
        def display_plot2():
        # Fetch from the reactive calc function
            deque_snapshot, df, latest_dictionary_entry = reactive_tips_combined()

            # Ensure the DataFrame is not empty before plotting
            if not df.empty:
                # Convert the 'timestamp' column to datetime for better plotting
                df["timestamp"] = pd.to_datetime(df["timestamp"])

        
            fig = px.scatter(df,
            x="timestamp",
            y="boyamnt",
            title="Recorded Female Tips with Regression Line",
            labels={"timestamp": "Time", "boyamnt": "Tips"},
            color_discrete_sequence=["orange"] )
            
          

            # For x let's generate a sequence of integers from 0 to len(df)
            sequence = range(len(df))
            x_vals = list(sequence)
            y_vals = df["boyamnt"]

            slope, intercept, r_value, p_value, std_err = stats.linregress(x_vals, y_vals)
            df['best_fit_line'] = [slope * x + intercept for x in x_vals]

            # Add the regression line to the figure
            fig.add_scatter(x=df["timestamp"], y=df['best_fit_line'], mode='lines', name='Regression Line')

            #update layout as neeted to customize further
            fig.update_layout(xaxis_title="Time", yaxis_title="Tip Amount $")
            fig.update_layout(height=300)
    
            return fig
        

 
   
#REACTIVE CALULCATIONS-----------------------------------------------------
@reactive.calc
def filtered_dining_time():
    req(input.selected_dining_time())
    isTipsMatch=tips["time"].isin(input.selected_dining_time())
    return tips[isTipsMatch]

def filtered_gender():
    req(input.selected_gender())
    isGenderMatch=tips["sex"].isin(input.selected_gender())
    return tips[isGenderMatch]
    
def filtered_tips_and_gender():
    filt_df = tips[tips["time"].isin(input.selected_dining_time())]
    filt_df=filt_df[filt_df['sex'].isin(input.selected_gender())]
    filt_df=filt_df[filt_df['total_bill'].between(input.total_bill_amount()[0], input.total_bill_amount()[1])]
    return filt_df

    
def reactive_tips_combined():
    reactive.invalidate_later(UPDATE_INTERVAL_SECS) #Invalidate to trigger updates
    #DATA GENERATION
    tip_value_girls=round(random.uniform(1,50),1)
    tip_value_boys=round(random.uniform(1,50),1)
    timestamp_value=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_date_time={"girlamnt":tip_value_girls, "boyamnt":tip_value_boys, "timestamp":timestamp_value}

    #append the deque
    reactive_value_wrapper.get().append(new_date_time)

    #Get a snapshot
    deque_snapshot = reactive_value_wrapper.get()

    #convert deque to dataframe
    df = pd.DataFrame(deque_snapshot)

    #Display latest dictionary entry
    latest_dictionary_entry= new_date_time

    #return values needed
    return deque_snapshot, df, latest_dictionary_entry




    


    
