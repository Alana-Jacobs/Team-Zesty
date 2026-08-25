import pandas as pd 

def clean_data(df):
    # Drop duplicates
    df = df.drop_duplicates()

    # Drop missing comments
    df = df.dropna(subset=['comment_text'])

    # Remove non-alphanumeric characters
    df['comment_text'] = df['comment_text'].str.replace(r'[^0-9a-zA-Z\s.,!?/]', '', regex=True)

    # Normalize whitespace
    df['comment_text'] = df['comment_text'].str.replace(r'\s+', ' ', regex=True).str.strip()

     # Remove junk comments
    junk_comments = ['no comment.', 'same as last time', 'see attached', 'test entry please ignore']    
    df = df[~df['comment_text'].str.strip().str.lower().isin(junk_comments)]

    # Remove comments that are too short to be meaningful
    df = df[df['comment_text'].str.len() > 5]

    # Remove comments that are only numbers or punctuation
    df = df[df['comment_text'].str.contains('[a-zA-Z]{3,}', na=False, regex=True)]

    # Normalize case
    df['comment_text'] = df['comment_text'].str.lower()

    # Standardize date format
    df['created_at'] = pd.to_datetime(df['created_at'], dayfirst=True, errors='coerce')

    # Drop duplicates after cleaning and reset index once
    df = df.drop_duplicates().reset_index(drop=True)

    if df.empty:
        raise ValueError("No valid comments available after cleaning.")

    return df
