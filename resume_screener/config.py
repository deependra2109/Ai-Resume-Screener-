"""
Central configuration for the AI Resume Screener.
Keep magic strings/numbers here so nothing is duplicated across modules.
"""

# ---- NLP models ----
SPACY_MODEL = "en_core_web_sm"
SENTENCE_TRANSFORMER_MODEL = "all-MiniLM-L6-v2"   # small, fast, good enough for this use case

# ---- Gemini (LLM) ----
GEMINI_MODEL = "gemini-2.5-flash"   # gemini-2.0-flash is deprecated, do not use it

# ---- Scoring weights ----
# Final score = TFIDF_WEIGHT * tfidf_score + SEMANTIC_WEIGHT * semantic_score
# Semantic embeddings understand meaning/context, TF-IDF rewards exact keyword overlap.
# Blending both is more robust than either alone.
TFIDF_WEIGHT = 0.4
SEMANTIC_WEIGHT = 0.6

# ---- Skill keyword list ----
# You can expand this list anytime.
SKILL_KEYWORDS = {
    "python", "java", "c++", "c#", "javascript", "typescript",
    "html", "css", "react", "angular", "vue",
    "django", "flask", "spring", "spring boot", "node", "node.js",
    "sql", "mysql", "postgresql", "mongodb",
    "machine learning", "deep learning", "nlp",
    "pandas", "numpy", "scikit-learn", "tensorflow", "pytorch",
    "data analysis", "data science", "power bi", "tableau",
    "git", "docker", "kubernetes", "aws", "azure", "gcp",
}

# ---- Limits (basic safety/UX) ----
MAX_RESUMES = 25
MAX_PDF_SIZE_MB = 10
