import pandas as pd 

def clean_data(df):
    # Drop duplicates
    df = df.drop_duplicates().reset_index(drop=True)

    # Drop missing comments
    df = df.dropna(subset=['comment_text']).reset_index(drop=True)

    # Remove junk comments
    junk_comments = ['no comment.', 'same as last time', 'see attached', 'test entry please ignore']    
    df = df[~df['comment_text'].str.strip().str.lower().isin(junk_comments)].reset_index(drop=True)

    # Remove non-alphanumeric characters
    df['comment_text'] = df['comment_text'].str.replace(r'[^0-9a-zA-Z\s.,!?/]', '', regex=True)

    # Normalize whitespace
    df['comment_text'] = df['comment_text'].str.replace(r'\s+', ' ', regex=True).str.strip()

    # Remove comments that are too short to be meaningful
    df = df[df['comment_text'].str.len() > 5].reset_index(drop=True)

    # Normalize case
    df['comment_text'] = df['comment_text'].str.lower()

    # Standardize date format
    df['created_at'] = pd.to_datetime(df['created_at'], dayfirst=True, errors='coerce')

    # Drop duplicates after cleaning
    df = df.drop_duplicates().reset_index(drop=True)

    return df
