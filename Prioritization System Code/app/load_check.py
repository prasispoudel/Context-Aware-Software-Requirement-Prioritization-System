from fastapi import APIRouter
from fastapi.responses import JSONResponse
#from app.model_loader import load_core_prioritization_model
from .model_loader import (
    load_core_prioritization_model,
    load_dependency_model,
    load_text_embedder
)

router = APIRouter()

# Load once and reuse
try:
    xgb_model, tfidf_vectorizer, _ = load_core_prioritization_model()
    dep_tokenizer, dep_model = load_dependency_model(model_dir="path/to/dependency/model")
    embedder = load_text_embedder()
except Exception as e:
    print("❌ Error loading models:", e)
    raise RuntimeError("Model loading failed.")

@router.get("/status")
def health_check():
    try:
        xgb_features = xgb_model.get_booster().feature_names
        dependency_model_ok = dep_model is not None and hasattr(dep_model, "eval")
        return JSONResponse(
            status_code=200,
            content={
                "status": "OK",
                "prioritization_model_loaded": True,
                "dependency_model_loaded": dependency_model_ok,
                "tfidf_vectorizer_loaded": tfidf_vectorizer is not None,
                "text_embedder_loaded": embedder is not None,
                "xgboost_features": xgb_features,
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "status": "ERROR",
                "message": f"Model check failed: {str(e)}"
            }
        )
