from textblob import TextBlob
import pandas as pd

def analyse_sentiment(df):
    # Additional cleaning step for safety
    df = df.dropna(subset=['comment_text']).reset_index(drop=True)
    
    # Calculate sentiment scores and applies labels
    df['sentiment_score'] = df['comment_text'].apply(lambda x: TextBlob(x).sentiment.polarity)
    df['sentiment_label'] = df['sentiment_score'].apply(lambda x: 'positive' if x > 0 else ('negative' if x < 0 else 'neutral'))
    return df
