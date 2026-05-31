import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from textblob import TextBlob
from clean_data import clean_data
from sentiment import analyse_sentiment

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
    df = analyse_sentiment(df)
    st.success("Dataset uploaded successfully!")

    # Data cleaning summary
    with st.expander("Data Cleaning Summary"):
        st.write(f"Number of entries before cleaning: {before_cleaning}")
        st.write(f"Number of entries after cleaning: {len(df)}")
        st.write(f"Number of entries removed: {before_cleaning - len(df)}")

    # Sentiment analysis results
    st.subheader("Sentiment Analysis Results")
    st.caption("Sentiment analysis results are potential indicators gathered from your dataset and should not be interepreted as definitive view of customer sentiment.")

    # Sentiment distribution chart
    fig, ax = plt.subplots()
    sentiment_order = ['positive', 'neutral', 'negative']
    distribution = df['sentiment_label'].value_counts().reindex(sentiment_order)
    distribution.plot(kind='bar', ax=ax, color=['green', 'grey', 'red'])
    ax.set_title("Sentiment Distribution")
    ax.set_xlabel("Customer Sentiment")
    ax.set_ylabel("Comment Count")
    ax.set_xticklabels(sentiment_order, rotation=0)
    st.pyplot(fig)
    plt.close(fig)

    # Sentiment trends over time
    data_trends = df[['created_at', 'sentiment_score']].dropna()
    data_trends = data_trends.sort_values('created_at')
    data_trends = data_trends.set_index('created_at')
    data_trends = data_trends.resample('ME').mean()
    fig, ax = plt.subplots()
    data_trends['sentiment_score'].plot(ax=ax)
    ax.set_title("Sentiment Trends Over Time")
    ax.set_xlabel("Time")
    ax.set_ylabel("Average Sentiment Score")
    ax.axhline(y=0, color='grey', linestyle='--', label='Neutral sentiment', alpha=0.4)
    ax.legend()
    st.pyplot(fig)
    plt.close(fig)
        
    # Display random sample of comments
    st.write("Random Sample of Comments:")
    st.dataframe(df[['comment_text']].sample(min(5, len(df))), hide_index=True)
