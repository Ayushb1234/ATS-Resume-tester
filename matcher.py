from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import spacy
import os

# Load spaCy model with fallback
# try:
#     nlp = spacy.load("en_core_web_sm")
# except:
#     os.system("python -m spacy download en_core_web_sm")
#     nlp = spacy.load("en_core_web_sm")

nlp = spacy.load("en_core_web_sm")


# Load Sentence Transformer model (MiniLM)
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_match_score(resume_text, job_description):
    """
    Returns cosine similarity score between resume and job description.
    """
    if not resume_text.strip() or not job_description.strip():
        return 0.0
    embeddings = model.encode([resume_text, job_description], convert_to_tensor=True)
    score = cosine_similarity(embeddings[0:1], embeddings[1:2])[0][0]
    return float(score)

def extract_keywords_from_job_desc(text, top_n=10):
    """
    Extracts top keywords from a job description using spaCy.
    Filters out stopwords, punctuation, and irrelevant POS tags.
    """
    doc = nlp(text)
    keywords = [
        token.text.lower() for token in doc
        if token.is_alpha and not token.is_stop and token.pos_ in ['NOUN', 'PROPN', 'VERB']
    ]
    freq = {}
    for word in keywords:
        freq[word] = freq.get(word, 0) + 1
    sorted_keywords = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    return [kw for kw, _ in sorted_keywords[:top_n]]
