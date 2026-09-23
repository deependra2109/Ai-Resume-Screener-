

import streamlit as st
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from config import SENTENCE_TRANSFORMER_MODEL, TFIDF_WEIGHT, SEMANTIC_WEIGHT


@st.cache_resource(show_spinner="Loading semantic embedding model (first run only)...")
def load_embedding_model():
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer(SENTENCE_TRANSFORMER_MODEL)


def compute_tfidf_scores(resume_texts: list[str], job_description_text: str) -> list[float]:
    corpus = [job_description_text] + resume_texts
    try:
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(corpus)
        jd_vector = tfidf_matrix[0:1]
        resume_vectors = tfidf_matrix[1:]
        similarities = cosine_similarity(jd_vector, resume_vectors).flatten()
        return [float(s) for s in similarities]
    except ValueError:
        return [0.0] * len(resume_texts)


def compute_semantic_scores(resume_texts: list[str], job_description_text: str) -> list[float]:
   
    model = load_embedding_model()

    jd_embedding = model.encode([job_description_text], normalize_embeddings=True)
    resume_embeddings = model.encode(resume_texts, normalize_embeddings=True)

    similarities = cosine_similarity(jd_embedding, resume_embeddings).flatten()
    return [float(max(0.0, s)) for s in similarities]


def compute_blended_scores(
    cleaned_resumes: list[str],
    cleaned_jd: str,
    raw_resumes: list[str],
    raw_jd: str,
) -> list[dict]:
    tfidf_scores = compute_tfidf_scores(cleaned_resumes, cleaned_jd)
    semantic_scores = compute_semantic_scores(raw_resumes, raw_jd)

    results = []
    for t, s in zip(tfidf_scores, semantic_scores):
        blended = TFIDF_WEIGHT * t + SEMANTIC_WEIGHT * s
        results.append({"tfidf": t, "semantic": s, "blended": blended})
    return results
