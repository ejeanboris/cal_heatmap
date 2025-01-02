import pandas as pd 
import vobject
import requests
from datetime import datetime, date
import matplotlib.pyplot as plt
import calmap
import streamlit as st 
import plotly.express as px
import plotly.graph_objects as go
import json
import os



# Function to load data from a JSON file
def load_data(file_path):
    try:
        with open(file_path, 'r') as file:
            if os.path.getsize(file_path) == 0: return {}
            return json.load(file)
    except FileNotFoundError:
        print("settings file not found")
        return {}
    except :
        print("settings file invalid")
        return {}


# Function to save data to a JSON file
def save_data(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file)


# Function to create a calendar heatmap for a specific year
def create_calendar_heatmap(event_series, year):
    # Filter the series to include only the specific year
    event_series_year = event_series[event_series.index.year == year]

    # Create a complete date range for the year
    all_dates_year = pd.date_range(start=f'{year}-01-01', end=f'{year}-12-31')

    # Reindex the Series to include all dates in the year and fill missing dates with zero
    event_series_year = event_series_year.reindex(all_dates_year, fill_value=0)

    # Create a DataFrame for Plotly
    df_year = pd.DataFrame({'Date': event_series_year.index, 'Events': event_series_year.values})

    # Generate day of the week and week of the year
    df_year['DayOfWeek'] = df_year['Date'].dt.dayofweek
    df_year['WeekOfYear'] = df_year['Date'].dt.isocalendar().week
    df_year['Month'] = df_year['Date'].dt.strftime('%b')

    # Create the Plotly figure
    fig = go.Figure(data=go.Heatmap(
        z=df_year['Events'],
        x=df_year['WeekOfYear'],
        y=df_year['DayOfWeek'],
        colorscale='YlGn',
        showscale=True,
        colorbar=dict(
            title='# of Events',
            orientation='h',  # Set the color scale to horizontal
            len=0.3,  # Adjust the length of the color scale
            thickness=10,
            x=0.98,
            y=1,
            xanchor="right",
            yanchor="bottom",  # Position the color scale at the bottom
        ),
        hoverinfo='z+x+y'
    ))

    # Set the aspect ratio to ensure square boxes
    fig.update_yaxes(scaleanchor="x", scaleratio=1, constrain="domain")

    # Update the layout with the axes
    fig.update_layout(
        title=f'Calendar Heatmap for {year}',
        yaxis=dict(
            tickmode='array',
            tickvals=[0, 1, 2, 3, 4, 5, 6],
            ticktext=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
            range=[-1.2, 6.5], # Adjust the range to eliminate space
            automargin=True, # Adjust margins automatically 
            domain=[0.1,0.95] # Use available space effectively
        ),
        xaxis=dict(
            tickmode='array',
            tickvals=list(range(1, 54)),
            ticktext=list(range(1, 54)),
            title=dict(
                text='Weeks of the Year',
                standoff=0
            ),
            title_standoff=0,  # Adjust the distance of the title from the axis
            tickangle=-90,  # Adjust the angle of the week numbers
            ticklen=2,
            side='top', # Display x-axis ticks above the heatmap
            automargin=True, # Adjust margins automatically
        ),
        autosize=True,
        margin=dict(
            l=50,
            r=50,
            b=30,  # Increase bottom margin to fit month names
            t=30,  # Increase top margin to fit week numbers
            pad=0
        ),
        height=450, # Fixed height to avoid excessive space
    )

    # Add month annotations with arrows at the bottom
    month_starts = df_year.iloc[:-10].groupby('Month')['WeekOfYear'].min().to_dict()
    for month, week in month_starts.items():
        fig.add_annotation(
            x=week,
            y=-0.5,  # Position below the x-axis
            text=month,
            showarrow=False,
            arrowhead=2,
            ax=week,
            ay=0,  # Position the arrow closer
            xref="x",
            yref="y",
            #font=dict(size=12, color="black"),
            xanchor='left',
            yanchor='top'
        )
    
    return fig


def save_load():
    st.session_state['options'].pop("New")
    save_data(settings_file, st.session_state['options'])
    st.session_state['options'] = load_data(settings_file)
    
def update_params():
    st.session_state['cal_url'] = st.session_state['options'][st.session_state['setup']]['cal_url']
    st.session_state['number_of_years'] = st.session_state['options'][st.session_state['setup']]['number_of_years']


# set webpage title
st.title("Yearly Activity Heatmaps")

# File path for data storage
settings_file = 'settings.json'
# Load persisted data if it exists; set default values otherwise
st.session_state['options'] = load_data(settings_file)
st.session_state['options']["New"] = {
    'cal_url':"https://canada-holidays.ca/ics?cd=true",
    'number_of_years': 3
    }

# Get the Calendar Export link and number of years from sidebar menu
st.sidebar.header("Settings")
st.session_state['setup'] = st.sidebar.selectbox("Choose a Setup:", st.session_state['options'].keys())
st.session_state['cal_url'] = st.sidebar.text_input("Enter The Calendar Export Link:", value=st.session_state['options'][st.session_state['setup']]['cal_url'])
st.session_state['number_of_years'] = st.sidebar.number_input("Enter the number of years:", min_value=1, max_value=10, value=st.session_state['options'][st.session_state['setup']]['number_of_years'])
update_params()
if(st.session_state['setup'] == "New"):
    setup_save_name = st.sidebar.text_input("Setup Save Name:", value='yahoo')
    st.session_state['options'][setup_save_name] = {
        'cal_url': st.session_state['cal_url'],
        'number_of_years': st.session_state['number_of_years']
    }
    st.sidebar.button("Save",on_click=save_load)


response = requests.get(st.session_state['cal_url'])
if response.status_code == 200:
    # Parse the .ics file
    cal = vobject.readOne(response.text)
else:
    print("Failed to download the file")




# Create a dictionary to store event counts by date
event_counts = {}
for component in cal.components():
    if component.name == "VEVENT":
        event_date = component.dtstart.value
        if isinstance(event_date, datetime):
            event_date = event_date.date()
        if event_date in event_counts:
            event_counts[event_date] += 1
        else:
            event_counts[event_date] = 1



# Convert the dictionary to a pandas Series
event_series = pd.Series(event_counts)
# Ensure the index is in datetime format
event_series.index = pd.to_datetime(event_series.index)


# Get the current year
current_year = datetime.now().year
# Create a list of years to plot
years_to_plot = [current_year - i for i in range(st.session_state['number_of_years'])]



# Plot each year's data
for year in years_to_plot:
    fig = create_calendar_heatmap(event_series, year)
    st.plotly_chart(fig)



