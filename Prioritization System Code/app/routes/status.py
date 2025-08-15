'''
from fastapi import APIRouter

router = APIRouter()

@router.get("/status")
async def health_check():
    return {"status": "API is running."}
'''

'''
from fastapi import APIRouter
from main import xgb_model, tfidf_vectorizer, scaler, dep_model, embedder
#from fastapi.responses import JSONResponse
#from app.model_loader import load_core_prioritization_model, load_dependency_model, load_text_embedder
router = APIRouter()

@router.get("/status")
def health_check():
    try:
        xgb_features = xgb_model.get_booster().feature_names if xgb_model else []
        return {
            "status": "OK",
            "xgboost_model_loaded": xgb_model is not None,
            "tfidf_vectorizer_loaded": tfidf_vectorizer is not None,
            "scaler_loaded": scaler is not None,
            "dependency_model_loaded": dep_model is not None,
            "embedder_loaded": embedder is not None,
            "xgboost_features": xgb_features
        }
    except Exception as e:
        return {
            "status": "ERROR",
            "message": str(e)
        }

'''
'''
from fastapi import APIRouter
from app import state

router = APIRouter()

@router.get("/status")
def health_check():
    try:
        xgb_features = state.xgb_model.get_booster().feature_names if state.xgb_model else []
        return {
            "status": "OK",
            "xgboost_model_loaded": state.xgb_model is not None,
            "tfidf_vectorizer_loaded": state.tfidf_vectorizer is not None,
            "scaler_loaded": state.scaler is not None,
            "dependency_model_loaded": state.dep_model is not None,
            "embedder_loaded": state.embedder is not None,
            "xgboost_features": xgb_features
        }
    except Exception as e:
        return {
            "status": "ERROR",
            "message": str(e)
        }
'''
from fastapi import APIRouter
from app import state

router = APIRouter()

@router.get("/status")
def health_check():
    try:
        xgb_features = state.xgb_model.get_booster().feature_names if state.xgb_model else []
        return {
            "status": "OK",
            "xgboost_model_loaded": state.xgb_model is not None,
            "tfidf_vectorizer_loaded": state.tfidf_vectorizer is not None,
            "scaler_loaded": state.scaler is not None,
            "dependency_model_loaded": state.dep_model is not None,
            "embedder_loaded": state.embedder is not None,
            "contextual_models_loaded": all([
                state.risk_model,
                state.urgency_model,
                state.complexity_model,
                state.business_value_model,
                state.implementation_effort_model,
                state.stakeholder_criticality_model,
                state.requirement_stability_model,
                state.security_sensitivity_model
            ]),
            "xgboost_features": xgb_features
        }
    except Exception as e:
        return {
            "status": "ERROR",
            "message": str(e)
        }
