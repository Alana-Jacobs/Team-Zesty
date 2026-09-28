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

    # Sidebar + theme filter + Comments display + Downloads
    with st.sidebar:
        st.header("Themes")
        theme_options = ["All"] + sorted(df["theme"].unique().tolist())
        selected_theme = st.pills("Filter by theme", theme_options)

        st.subheader("Theme Comments")
        selected_theme_comments = st.selectbox("View comments by theme", sorted(df["theme"].unique().tolist()))
        theme_comments = df[df["theme"] == selected_theme_comments][["comment_text"]].sample(min(5, len(df[df["theme"] == selected_theme_comments])))
        st.dataframe(theme_comments, hide_index=True)

        st.download_button(
            label="Export Filtered Comments as CSV",
            data=df[['comment_text', 'theme', 'sentiment_label']].to_csv(index=False).encode('utf-8'),
            file_name="filtered_comments.csv",
            mime="text/csv"
        )

    st.success("Dataset uploaded successfully!")

    with st.expander("Dashboard Summary"):
        st.markdown(f"**Dataset Summary**")
        st.write(f"Entries analysed: {len(df)}")
        st.write(f"Entries removed during cleaning: {before_cleaning - len(df)}")
        st.divider()
        st.markdown("**Sentiment Overview**")
        st.write(f"Positive: {len(df[df['sentiment_label'] == 'positive'])} comments")
        st.write(f"Neutral: {len(df[df['sentiment_label'] == 'neutral'])} comments")
        st.write(f"Negative: {len(df[df['sentiment_label'] == 'negative'])} comments")
        st.divider()
        st.markdown("**Top Themes**")
        st.dataframe(df['theme'].value_counts().reset_index().rename(columns={'theme': 'Theme', 'count': 'Count'}), hide_index=True)

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
