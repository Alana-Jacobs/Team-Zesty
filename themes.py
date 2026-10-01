themes = {
    "Login & Access": ["login", "mfa", "password", "sign in", "session", "reset", "permission", "access", "invalid", "locked", "credentials", "account"],
    "Performance": ["performance", "slow", "load", "timeout", "lag", "crash", "freeze", "speed", "latency", "sluggish", "unresponsive", "error", "bug", "glitch"],
    "Billing & Payment": ["invoice", "payment", "charge", "refund", "billing", "paid", "price", "cost", "checkout", "subscription", "plan", "credit card", "fee"],
    "Content & Information": ["incorrect", "outdated", "missing", "wrong", "update", "content", "information", "old links", "broken", "inaccurate", "misleading"],
    "Support Experience": ["support", "response", "ticket", "helpful", "follow", "unanswered", "generic", "unhelpful", "rude", "delay", "wait", "assistance"],
    "Usability": ["navigation", "confusing", "layout", "search", "find", "menu", "accessibility", "contrast", "font", "readability", "user-friendly", "interface"],
    "School & Course Content": ["course", "class", "lesson", "assignment", "syllabus", "curriculum", "material", "topic", "lecture", "exam", "grading", "feedback"],
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
