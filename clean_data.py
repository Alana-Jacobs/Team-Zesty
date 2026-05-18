import pandas as pd 

def clean_data(df):
    df = df.drop_duplicates().reset_index(drop=True)    # Drop duplicates

    df = df.dropna(subset=['comment_text']).reset_index(drop=True)  # Drop missing comments
    
    junk_comments = ['no comment.', 'same as last time', 'see attached', 'test entry please ignore']    # Remove junk comments
    df = df[~df['comment_text'].str.strip().str.lower().isin(junk_comments)].reset_index(drop=True)

    df = df[df['comment_text'].str.strip().str.len() > 5].reset_index(drop=True)    # Remove comments that are too short to be meaningful

    df['created_at'] = pd.to_datetime(df['created_at'], dayfirst=True, errors='coerce') # Standardize date format
    return df

