from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.status import router as status_router
from app.routes.prioritize import router as prioritize_router
from app.routes.dependencies import router as dependencies_router
from app import state
from app.model_loader import (
    load_core_prioritization_model,
    load_dependency_model,
    load_text_embedder,
    load_contextual_models
)

# Initialize FastAPI app
app = FastAPI(
    title="Context-Aware Requirement Prioritization System",
    version="1.0.0",
    description="Backend API for prioritizing software requirements using contextual and dependency-aware machine learning models."
)

# Allow frontend access (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === Load all ML models on startup ===
@app.on_event("startup")
def load_models():
    try:
        state.xgb_model, state.tfidf_vectorizer, state.scaler = load_core_prioritization_model()
        state.dep_tokenizer, state.dep_model = load_dependency_model()
        state.embedder = load_text_embedder()
        state.contextual_models = load_contextual_models()
        #state.risk_model = state.contextual_models['risk']
        #state.urgency_model = state.contextual_models['urgency']
        #state.complexity_model = state.contextual_models['complexity']
        #state.business_value_model = state.contextual_models['business_value']
        #state.implementation_effort_model = state.contextual_models['implementation_effort']
        #state.stakeholder_criticality_model = state.contextual_models['stakeholder_criticality']
        #state.requirement_stability_model = state.contextual_models['requirement_stability']
        #state.security_sensitivity_model = state.contextual_models['security_sensitivity']
        print(" All models loaded successfully.")
    except Exception as e:
        print(f"Error loading models: {e}")
        raise RuntimeError("Model loading failed. Check file paths and formats.")

# === Import routes after model loading ===
app.include_router(prioritize_router, prefix="/api")
app.include_router(dependencies_router, prefix="/api")
app.include_router(status_router, prefix="/api")

# === Run with: uvicorn main:app --reload ==
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

