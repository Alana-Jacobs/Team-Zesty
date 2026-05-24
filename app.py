import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from textblob import TextBlob
from clean_data import clean_data

st.title("Customer Sentiment and Theme Dashboard")

# Sidebar + theme filter
with st.sidebar:
    st.header("Themes")
    st.pills("Filter by theme", ["All"])
    
# Load CSV file
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    before_cleaning = len(df)
    df = clean_data(df)
    st.success("Dataset uploaded successfully!")

    # Data cleaning summary
    with st.expander("Data Cleaning Summary"):
        st.write(f"Number of entries before cleaning: {before_cleaning}")
        st.write(f"Number of entries after cleaning: {len(df)}")
        st.write(f"Number of entries removed: {before_cleaning - len(df)}")
        
    # Display random sample of comments
    st.write("Random Sample of Comments:")
    st.dataframe(df[['comment_text']].sample(min(5, len(df))), hide_index=True)
