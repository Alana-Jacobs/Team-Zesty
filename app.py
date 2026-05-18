import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from textblob import TextBlob
from clean_data import clean_data

st.title("Feedback Dashboard")

# Load CSV file
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    before_cleaning = len(df) # Validation
    df = clean_data(df)
    st.success("Dataset uploaded successfully!")

    with st.expander("Data Cleaning Summary"): # Validation
        st.write(f"Number of entries before cleaning: {before_cleaning}")
        st.write(f"Number of entries after cleaning: {len(df)}")
        st.markdown("- Removed duplicates")
        st.markdown("- Removed missing and junk comments")
        st.markdown("- Standardised date formats")

    st.write("Data Preview:")
    st.dataframe(df.head(10))
