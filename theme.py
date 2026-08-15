from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF

def extract_themes(df, text_col='comment_text', n_topics=5):
    tfidf = TfidfVectorizer(max_df=0.9, min_df=2, stop_words='english')
    X = tfidf.fit_transform(df[text_col])

    nmf = NMF(n_components=n_topics, random_state=42)
    W = nmf.fit_transform(X)
    H = nmf.components_

    terms = tfidf.get_feature_names_out()
    theme_labels = {
        i: ", ".join(terms[j] for j in topic.argsort()[-3:][::-1])
        for i, topic in enumerate(H)
    }

    df['theme'] = W.argmax(axis=1).astype(str) + ": " + \
        pd.Series(W.argmax(axis=1)).map(theme_labels).values
    return df, theme_labels