from fastapi import APIRouter
from app import state
from pydantic import BaseModel
from typing import Dict, Any, Optional, List 
import numpy as np
import os
router = APIRouter()


class RequirementInput(BaseModel):
    requirement_text: str
    contextual_features: List[float]  # Risk, urgency, etc.
    dependency_features: List[float]  # Num_Depends, Is_Leaf, etc.

class BatchRequirementInput(BaseModel):
    items: List[RequirementInput]


@router.post("/prioritize/batch")
def prioritize_batch(payload: BatchRequirementInput):
    try:
        req_texts = [item.requirement_text for item in payload.items]
        context_features = np.array([item.contextual_features for item in payload.items])
        dependency_features = np.array([item.dependency_features for item in payload.items])

        if state.tfidf_vectorizer is None or state.xgb_model is None:
            return {"error": "Model or vectorizer not loaded."}

        tfidf_matrix = state.tfidf_vectorizer.transform(req_texts)
        combined_input = np.hstack([tfidf_matrix.toarray(), context_features, dependency_features])
        predictions = state.xgb_model.predict(combined_input)

        return [
            {"requirement_text": req, "priority_score": round(float(score), 4)}
            for req, score in zip(req_texts, predictions)
        ]

    except Exception as e:
        return {"error": str(e)}



@router.post("/prioritize")
def start_prioritization(req: RequirementInput):
    try:
        # Vectorize requirement text
        if state.tfidf_vectorizer is None:
            return {"error": "TF-IDF vectorizer is not initialized."}
        tfidf = state.tfidf_vectorizer.transform([req.requirement_text])
        context = np.array(req.contextual_features).reshape(1, -1)
        deps = np.array(req.dependency_features).reshape(1, -1)

        combined_input = np.hstack([tfidf.toarray(), context, deps])
        if state.xgb_model is None:
            return {"error": "XGBoost model is not initialized."}
        prediction = state.xgb_model.predict(combined_input)[0]

        return {"priority_score": round(float(prediction), 4)}
    except Exception as e:
        return {"error": str(e)}
    


@router.get("/prioritize")
async def prioritize():
	return {"message": "Prioritization endpoint is working."}