import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from textblob import TextBlob

st.title("Streamlit Feasibility Test")

# CSV File Upload and Preview
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("Preview of the uploaded data:")
    st.dataframe(df.head())

# Simple Data Visualization
col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots()
    df['rating_1to5'].dropna().plot(kind='hist', ax=ax, bins=5)
    ax.set_title("Distribution of Ratings")
    ax.set_xlabel("Rating")
    ax.set_ylabel("Count")
    st.pyplot(fig)
    plt.close(fig)

with col2:
    fig, ax = plt.subplots()
    df['category'].value_counts().plot(kind='bar', ax=ax)
    ax.set_title("Feedback by Category")
    ax.set_xlabel("Category")
    ax.set_ylabel("Count")
    st.pyplot(fig)
    plt.close(fig)

# Sentiment Analysis
df['sentiment_score'] = df['comment_text'].dropna().apply(lambda x: TextBlob(x).sentiment.polarity)
fig, ax = plt.subplots()
df['sentiment_score'].plot(kind='hist', ax=ax, bins=10)
ax.set_title("Distribution of Sentiment Scores")
ax.set_xlabel("Sentiment Score")
ax.set_ylabel("Count")
st.pyplot(fig)
plt.close(fig)
