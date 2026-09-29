import re
from collections import Counter

import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# ============================================================
# VADER INITIALIZATION
# ============================================================

try:
    nltk.data.find("sentiment/vader_lexicon.zip")
except LookupError:
    nltk.download("vader_lexicon", quiet=True)

sentiment_analyzer = SentimentIntensityAnalyzer()


# ============================================================
# STOP WORDS
# ============================================================

STOP_WORDS = {
    "the", "is", "a", "an", "and", "or", "to", "of",
    "for", "in", "on", "at", "by", "with", "from",
    "my", "i", "me", "we", "our", "you", "your",
    "it", "this", "that", "was", "were", "are",
    "have", "has", "had", "been", "be", "being",
    "am", "do", "does", "did", "not", "but",
    "very", "can", "could", "would", "should",
    "please", "they", "them", "their", "there",
    "here", "as", "if", "so", "than", "then"
}


# ============================================================
# CATEGORY KNOWLEDGE BASE
# ============================================================

CATEGORY_DOCUMENTS = {

    "Delivery": """
    delivery delayed late package shipment courier parcel
    order not received delivery date tracking shipping
    delivery person delivery status missing package
    """

    ,

    "Payment": """
    payment transaction refund money charged billing invoice
    debit credit card payment failed payment deducted
    double charged wrong amount financial transaction
    """

    ,

    "Product": """
    product item damaged broken defective poor quality
    wrong product missing item product condition replacement
    product not working manufacturing defect
    """

    ,

    "Technical": """
    application app website software login account password
    technical error server crash bug system not working
    unable to login website loading technical problem
    """

    ,

    "Customer Service": """
    customer support representative agent service response
    phone call email support team complaint communication
    nobody responded customer care staff
    """

    ,

    "Account": """
    account profile registration verification password
    account blocked account locked login credentials
    username personal information account access
    """
}


# ============================================================
# TEXT PREPROCESSING
# ============================================================

def clean_text(text: str) -> str:
    """
    Basic NLP preprocessing.

    Steps:
    1. Convert text to lowercase
    2. Remove URLs
    3. Remove punctuation
    4. Remove extra spaces
    """

    text = text.lower()

    # Remove URLs
    text = re.sub(
        r"https?://\S+|www\.\S+",
        " ",
        text
    )

    # Keep alphabetic characters and numbers
    text = re.sub(
        r"[^a-zA-Z0-9\s]",
        " ",
        text
    )

    # Remove extra whitespace
    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# ============================================================
# TOKENIZATION
# ============================================================

def tokenize(text: str) -> list[str]:
    """
    Tokenizes cleaned text and removes stopwords.
    """

    cleaned = clean_text(text)

    tokens = cleaned.split()

    tokens = [
        token
        for token in tokens
        if token not in STOP_WORDS
        and len(token) > 2
    ]

    return tokens


# ============================================================
# SENTIMENT ANALYSIS
# ============================================================

def analyze_sentiment(text: str) -> dict:
    """
    Uses VADER sentiment analysis.

    Returns:
        sentiment label
        compound score
        positive score
        neutral score
        negative score
    """

    scores = sentiment_analyzer.polarity_scores(text)

    compound = scores["compound"]

    if compound >= 0.05:
        label = "Positive"

    elif compound <= -0.05:
        label = "Negative"

    else:
        label = "Neutral"

    return {
        "label": label,
        "compound": round(compound, 3),
        "positive": round(scores["pos"], 3),
        "neutral": round(scores["neu"], 3),
        "negative": round(scores["neg"], 3)
    }


# ============================================================
# CATEGORY CLASSIFICATION
# ============================================================

def classify_complaint(text: str) -> dict:
    """
    Classifies a complaint using TF-IDF and cosine similarity.

    The complaint is compared against category knowledge
    documents representing different complaint types.
    """

    categories = list(CATEGORY_DOCUMENTS.keys())

    documents = list(CATEGORY_DOCUMENTS.values())

    complaint_cleaned = clean_text(text)

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2)
    )

    all_documents = documents + [complaint_cleaned]

    matrix = vectorizer.fit_transform(all_documents)

    category_vectors = matrix[:-1]
    complaint_vector = matrix[-1]

    similarities = cosine_similarity(
        complaint_vector,
        category_vectors
    )[0]

    scores = {
        category: round(float(score), 3)
        for category, score
        in zip(categories, similarities)
    }

    best_index = similarities.argmax()

    category = categories[best_index]

    confidence = float(similarities[best_index])

    # If similarity is extremely low, don't force a category
    if confidence < 0.05:
        category = "General"

    return {
        "category": category,
        "confidence": round(confidence, 3),
        "scores": scores
    }


# ============================================================
# URGENCY DETECTION
# ============================================================

HIGH_URGENCY_TERMS = {
    "urgent",
    "immediately",
    "emergency",
    "asap",
    "critical",
    "fraud",
    "stolen",
    "blocked",
    "unauthorized",
    "security",
    "danger",
    "unsafe"
}


MEDIUM_URGENCY_TERMS = {
    "delay",
    "delayed",
    "waiting",
    "problem",
    "issue",
    "failed",
    "failure",
    "broken",
    "not working",
    "complaint"
}


def detect_urgency(text: str) -> dict:
    """
    Estimates urgency using explicit urgency indicators.
    """

    cleaned = clean_text(text)

    high_matches = [
        term
        for term in HIGH_URGENCY_TERMS
        if term in cleaned
    ]

    medium_matches = [
        term
        for term in MEDIUM_URGENCY_TERMS
        if term in cleaned
    ]

    if high_matches:
        level = "High"

    elif medium_matches:
        level = "Medium"

    else:
        level = "Low"

    return {
        "level": level,
        "indicators": high_matches + medium_matches
    }


# ============================================================
# KEYWORD EXTRACTION
# ============================================================

def extract_keywords(text: str, max_keywords: int = 8) -> list[str]:
    """
    Extracts frequent meaningful terms from the complaint.
    """

    tokens = tokenize(text)

    if not tokens:
        return []

    frequencies = Counter(tokens)

    keywords = [
        word
        for word, count
        in frequencies.most_common(max_keywords)
    ]

    return keywords


# ============================================================
# COMPLETE NLP ANALYSIS
# ============================================================

def analyze_complaint(text: str) -> dict:
    """
    Runs the complete ComplaintIQ NLP pipeline.
    """

    if not text or not text.strip():
        raise ValueError("Complaint text cannot be empty.")

    cleaned = clean_text(text)

    tokens = tokenize(text)

    sentiment = analyze_sentiment(text)

    classification = classify_complaint(text)

    urgency = detect_urgency(text)

    keywords = extract_keywords(text)

    return {
        "original_text": text,
        "cleaned_text": cleaned,
        "tokens": tokens,
        "token_count": len(tokens),
        "sentiment": sentiment,
        "classification": classification,
        "urgency": urgency,
        "keywords": keywords
    }