import streamlit as st
import pandas as pd
import plotly.express as px

# Set up the web page layout
st.set_page_config(page_title="Admin Console", layout="wide")
st.title("🏢 Admin Console Analytics Dashboard")

# --- FILE UPLOAD COMPONENT ---
st.sidebar.header("Data Upload")
st.sidebar.write("Upload a new file to update the dashboard instantly.")
uploaded_file = st.sidebar.file_uploader("Upload Excel File", type=["xlsx", "xls"])

# Determine which file to use (the uploaded one, or the default one from GitHub)
file_to_read = uploaded_file if uploaded_file else "Admin Console _ FY26_27.xlsx"

# --- UPDATED & MORE ROBUST DATA LOADING ---
sheet_to_load = "Monthly Bills" # The sheet name we are trying to load

try:
    # Read the specified sheet
    df = pd.read_excel(file_to_read, sheet_name=sheet_to_load, header=1)
    
    st.success("Successfully loaded the dashboard!")

    # Display Key Metrics
    st.subheader("Key Performance Indicators")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Locations", df['Location'].nunique())
    col2.metric("Total Vendors", df['Vendor'].nunique())
    col3.metric("Service Types", df['Service type'].nunique())

    # Display the Raw Data Table
    st.subheader("Monthly Bills Data")
    st.dataframe(df, use_container_width=True)

    # Basic Chart: Count of services by location
    st.subheader("Services per Location")
    location_counts = df['Location'].value_counts().reset_index()
    location_counts.columns = ['Location', 'Count']
    
    fig = px.bar(location_counts, x='Location', y='Count', color='Location', title="Number of Services by Location")
    st.plotly_chart(fig, use_container_width=True)

except ValueError as e:
    # This block runs if the worksheet is not found
    st.error(f"Error: Worksheet named '{sheet_to_load}' not found.")
    try:
        # Try to read all sheet names from the Excel file to help with debugging
        xls = pd.ExcelFile(file_to_read)
        st.info("The available sheets in your Excel file are:")
        st.write(xls.sheet_names)
        st.warning(f"Please update the `sheet_to_load` variable in the `app.py` file to one of the names listed above and commit the change.")
    except Exception as inner_e:
        st.error(f"Additionally, an error occurred while trying to read the sheet names: {inner_e}")
except Exception as e:
    # Catch any other general errors
    st.error(f"An unexpected error occurred while loading the data: {e}")

