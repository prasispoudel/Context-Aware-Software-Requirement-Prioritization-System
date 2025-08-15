# app/state.py

xgb_model = None
tfidf_vectorizer = None
scaler = None

dep_tokenizer = None
dep_model = None

embedder = None
contextual_models = {}

risk_model = None
urgency_model = None
complexity_model = None
business_value_model = None
implementation_effort_model = None
stakeholder_criticality_model = None
requirement_stability_model = None
security_sensitivity_model = None
# This module holds global state for loaded models
# This allows us to access models across different routes without reloading them
# This is useful for performance and memory efficiency in a FastAPI application
# Models are loaded once at startup and reused for each request