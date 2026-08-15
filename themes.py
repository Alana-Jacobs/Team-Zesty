themes = {
    "Delivery": ["delivery", "shipping", "late", "arrived", "package"],
    "Customer Service": ["service", "support", "staff", "helpful", "communication"],
    "Product Quality": ["quality", "product", "broken", "defective", "damaged"],
    "Price": ["price", "expensive", "cheap", "cost", "value"],
    "Purchase": ["buy", "purchase", "order", "recommend"]
}


def extract_themes(df):

    def find_theme(comment):
        comment = str(comment).lower()

        for theme, keywords in themes.items():
            for keyword in keywords:
                if keyword in comment:
                    return theme

        return "Other"

    df["theme"] = df["comment_text"].apply(find_theme)

    return df