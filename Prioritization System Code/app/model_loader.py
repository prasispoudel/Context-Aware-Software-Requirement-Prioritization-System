import os
import pickle
from typing import Dict

import xgboost as xgb
from sklearn.feature_extraction.text import TfidfVectorizer
from transformers import RobertaTokenizer, RobertaForSequenceClassification
try:
    from tensorflow.keras.models import load_model # type: ignore
except ImportError:
    from keras.models import load_model
from sentence_transformers import SentenceTransformer

import joblib
import pickle

'''
# === Core Prioritization Model ===
def load_core_prioritization_model(model_dir="models/prioritization/"):
    model_path = os.path.join(model_dir, "Tuned_XGBoost_(Bayesian_Opt)_model.joblib")
    vectorizer_path = os.path.join(model_dir, "tfidf_vectorizer.joblib")
    scaler_path = os.path.join(model_dir, "scaler.joblib")

    model = joblib.load(model_path)
    vectorizer = joblib.load(vectorizer_path)
    scaler = joblib.load(scaler_path)

    return model, vectorizer, scaler

# === Dependency Estimation Model (RoBERTa) ===
from transformers import RobertaTokenizer, RobertaForSequenceClassification
import torch

def load_dependency_model(model_dir: str):
    tokenizer = RobertaTokenizer.from_pretrained(model_dir)
    model = RobertaForSequenceClassification.from_pretrained(model_dir)
    model.eval()
    return tokenizer, model


# === Optional: Sentence Embedding Loader (e.g., USE) ===
def load_text_embedder(model_name="sentence-transformers/all-mpnet-base-v2"):
    return SentenceTransformer(model_name)
    '''

'''
import os
import joblib
from typing import Dict
import torch
from sklearn.feature_extraction.text import TfidfVectorizer
from transformers import RobertaTokenizer, RobertaForSequenceClassification

try:
    from tensorflow.keras.models import load_model
except ImportError:
    from keras.models import load_model

from sentence_transformers import SentenceTransformer
'''
# === Core Prioritization Model ===
def load_core_prioritization_model(model_dir="models/prioritization/"):
    model_path = os.path.join(model_dir, "Tuned_XGBoost_(Bayesian_Opt)_model.joblib")
    vectorizer_path = os.path.join(model_dir, "tfidf_vectorizer.joblib")
    scaler_path = os.path.join(model_dir, "scaler.joblib")

    if not all(os.path.exists(p) for p in [model_path, vectorizer_path, scaler_path]):
        raise FileNotFoundError("Missing one or more core prioritization model files.")

    model = joblib.load(model_path)
    vectorizer = joblib.load(vectorizer_path)
    scaler = joblib.load(scaler_path)

    return model, vectorizer, scaler

# === Dependency Estimation Model (RoBERTa) ===
def load_dependency_model(model_dir="models/dependency/"):
    if not os.path.exists(model_dir):
        raise FileNotFoundError("Dependency model folder not found.")

    tokenizer = RobertaTokenizer.from_pretrained(model_dir)
    model = RobertaForSequenceClassification.from_pretrained(model_dir)
    model.eval()
    return tokenizer, model

# === Text Embedding Model (e.g., for context inference) ===
def load_text_embedder(model_name="sentence-transformers/all-mpnet-base-v2"):
    try:
        embedder = SentenceTransformer(model_name)
        return embedder
    except Exception as e:
        raise RuntimeError(f"Failed to load text embedding model: {e}")

def load_contextual_models(model_dir="models/contextual/"):
    # from tensorflow.keras.models import load_model
    # from transformers import RobertaTokenizer, RobertaForSequenceClassification
    # import os s

    models = {}

    # Load risk model and tokenizer (RoBERTa-based)
    risk_model_path = os.path.join(model_dir, "risk_roberta")
    models['risk'] = {
        "model": RobertaForSequenceClassification.from_pretrained(risk_model_path),
        "tokenizer": RobertaTokenizer.from_pretrained(risk_model_path)
    }

    # Load other contextual feature models (USE + Keras)
    models['urgency'] = load_model(os.path.join(model_dir, "final_urgency_model.keras"))
    models['complexity'] = load_model(os.path.join(model_dir, "final_complexity_model.keras"))
    models['business_value'] = load_model(os.path.join(model_dir, "final_business_value_model.keras"))
    models['implementation_effort'] = load_model(os.path.join(model_dir, "final_implementation_effort_model.keras"))
    models['stakeholder_criticality'] = load_model(os.path.join(model_dir, "final_stakeholder_criticality_model.keras"))
    models['requirement_stability'] = load_model(os.path.join(model_dir, "final_requirement_stability_model.keras"))
    models['security_sensitivity'] = load_model(os.path.join(model_dir, "final_security_sensitivity_model.keras"))

    return models

