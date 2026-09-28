import streamlit as st
import pandas as pd
import plotly.express as px
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

    try:
        df = clean_data(df)
    except ValueError as e:
        st.error(f"Error occurred while cleaning data: {e}")
        st.stop()

    try:
        df = analyse_sentiment(df)
    except ValueError as e:
        st.error(f"Error occurred while analysing sentiment: {e}")
        st.stop()

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
    sentiment_order = ['positive', 'neutral', 'negative']
    distribution = df['sentiment_label'].value_counts().reindex(sentiment_order).reset_index()
    distribution.columns = ['Sentiment', 'Count']
    fig = px.bar(distribution, x='Sentiment', y='Count', color='Sentiment',
                color_discrete_map={'positive': 'green', 'neutral': 'grey', 'negative': 'red'},
                title='Sentiment Distribution')
    st.plotly_chart(fig)

    # Sentiment trends over time
    data_trends = df[['created_at', 'sentiment_score']].dropna()
    data_trends = data_trends.sort_values('created_at')
    data_trends = data_trends.set_index('created_at')
    data_trends = data_trends.resample('ME').mean().reset_index()

    if not data_trends.empty:
        fig = px.line(data_trends, x='created_at', y='sentiment_score',
                    title='Sentiment Trends Over Time',
                    labels={'created_at': 'Date', 'sentiment_score': 'Average Sentiment Score'})
        fig.add_hline(y=0, line_dash='dash', line_color='grey', opacity=0.4, annotation_text='Neutral')
        fig.update_xaxes(rangeslider_visible=True)
        st.plotly_chart(fig)
    else:
        st.info("Not enough date data to display trend chart for this theme filter.")

    # Themes over time
    st.subheader("Themes Over Time")
    theme_trends = df[['created_at', 'theme']].dropna()
    theme_trends = theme_trends.sort_values('created_at')
    theme_trends['month'] = theme_trends['created_at'].dt.to_period('M').dt.to_timestamp()
    theme_trends = theme_trends.groupby(['month', 'theme']).size().reset_index(name='count')

    if not theme_trends.empty:
        fig = px.line(theme_trends, x='month', y='count', color='theme',
                      title='Theme Trends Over Time',
                      labels={'month': 'Date', 'count': 'Comment Count', 'theme': 'Theme'})
        fig.update_xaxes(rangeslider_visible=True)
        st.plotly_chart(fig)
    else:
        st.info("Not enough date data to display theme trends")    

    # Display random sample of comments
    with st.expander("Random Sample of Comments"):
        st.dataframe(df[['comment_text']].sample(min(5, len(df))), hide_index=True)
