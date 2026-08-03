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

try:
    # Read the Monthly Bills sheet (skipping the complex headers for a simple view)
    df = pd.read_excel(file_to_read, sheet_name="Monthly_Bills_", header=1)
    
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

except Exception as e:
    st.error(f"Error loading the data: {e}")
    st.info("Please make sure the Excel file has a sheet named 'Monthly_Bills_'")
