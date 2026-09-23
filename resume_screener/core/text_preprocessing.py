

import string
import streamlit as st
import spacy
import nltk

from config import SPACY_MODEL


@st.cache_resource(show_spinner="Loading NLP models (first run only)...")
def load_nlp_resources():
    nltk.download("stopwords", quiet=True)
    from nltk.corpus import stopwords

    nlp = spacy.load(SPACY_MODEL)
    stop_words = set(stopwords.words("english"))
    return nlp, stop_words


def preprocess_text(text: str) -> str:
    if not text:
        return ""

    nlp, stop_words = load_nlp_resources()

    text = text.lower()
    doc = nlp(text)

    clean_tokens = [
        token.text
        for token in doc
        if token.text not in stop_words and token.text not in string.punctuation
    ]
    return " ".join(clean_tokens)
