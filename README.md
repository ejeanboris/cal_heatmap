# cal_heatmap: Yearly Calendar Heatmaps

This project generates interactive yearly activity heatmaps using calendar data from a specified URL. It utilizes Streamlit for the web interface, Plotly for creating heatmaps, and other supporting libraries for data handling and visualization.

## Features
- Load calendar data from a given URL.
- Save and load different configurations for calendar URL and number of years to display.
- Generate interactive yearly heatmaps of events.
- Customize the number of years to visualize.

## Prerequisites

- Python 3.9+
- Required Python packages (listed in `requirements.txt`)!

## Installation

1. **Clone the repository:**

```sh
git clone https://github.com/yourusername/yearly-activity-heatmaps.git
cd yearly-activity-heatmaps
```

2. **Install the required packages:**

```sh
pip install -r requirements.txt
```

3. **Run the Streamlit app:**

```sh
streamlit run app.py
```

## Usage

1. **Configure Settings:**
   - Enter the calendar export link.
   - Set the number of years to visualize.
   - Save your configuration.

2. **Generate Heatmaps:**
   - The app will download the calendar data.
   - It will parse the data and count events for each day.
   - Interactive heatmaps will be generated for the specified years.

## File Structure

- `app.py`: Main script for running the Streamlit app.
- `settings.json`: JSON file to store user configurations.
- `requirements.txt`: List of required Python packages.

## Project Dependencies

Make sure you have the following Python libraries installed:

- pandas
- vobject
- requests
- datetime
- matplotlib
- calmap
- streamlit
- plotly

You can install all dependencies using the following command:

```sh
pip install -r requirements.txt
```

## Docker Deployment

1. **Build Docker Image:**

```sh
docker build -t yearly-activity-heatmaps .
```

2. **Run Docker Container:**

```sh
docker run -p 8501:8501 yearly-activity-heatmaps
```

This will build and run your Streamlit app inside a Docker container, exposing it on port 8501.

## Example Code

Below is a snippet of the core functionality in `app.py`:

```python
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

# Functions to load and save data, create heatmaps, and update session state...

# Set webpage title
st.title("Yearly Activity Heatmaps")

# Main logic for loading configurations, downloading calendar data, and generating heatmaps...

# Plot each year's data
for year in years_to_plot:
    fig = create_calendar_heatmap(event_series, year)
    st.plotly_chart(fig)
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Streamlit for providing a fantastic framework for building web apps.
- Plotly for interactive data visualization capabilities.
- All contributors and users for their support.
