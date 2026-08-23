import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from textblob import TextBlob
from clean_data import clean_data
from sentiment import analyse_sentiment
from themes import extract_themes


st.title("Customer Sentiment and Theme Dashboard")

# Load CSV file
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    before_cleaning = len(df)
    df = clean_data(df)
    df = analyse_sentiment(df)
    df = extract_themes(df)

    # Sidebar + theme filter
    with st.sidebar:
        st.header("Themes")
        theme_options = ["All"] + sorted(df["theme"].unique().tolist())
        selected_theme = st.pills("Filter by theme", theme_options)

    if selected_theme and selected_theme != "All":
        df = df[df["theme"] == selected_theme]

    st.success("Dataset uploaded successfully!")

    with st.expander("Theme Extraction Summary"):
        st.dataframe(
            df[["comment_text", "theme"]],
            hide_index=True
        )

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

    if not data_trends.empty:
        fig, ax = plt.subplots()
        data_trends['sentiment_score'].plot(ax=ax)
        ax.set_title("Sentiment Trends Over Time")
        ax.set_xlabel("Time")
        ax.set_ylabel("Average Sentiment Score")
        ax.axhline(y=0, color='grey', linestyle='--', label='Neutral sentiment', alpha=0.4)
        ax.legend()
        st.pyplot(fig)
        plt.close(fig)
    else:
        st.info("Not enough date data to display trend chart for this theme filter.")

    # Display random sample of comments
    with st.expander("Random Sample of Comments"):
        st.dataframe(df[['comment_text']].sample(min(5, len(df))), hide_index=True)
