from fastapi import APIRouter
from pydantic import BaseModel
from transformers import RobertaTokenizer, RobertaForSequenceClassification
import torch
import os
import torch.nn.functional as F
from app import state
from typing import List
import numpy as np
router = APIRouter()

# ==== Dependency model and tokenizer (loaded once) ====
MODEL_DIR = "models/dependency"
tokenizer = RobertaTokenizer.from_pretrained(MODEL_DIR)
model = RobertaForSequenceClassification.from_pretrained(MODEL_DIR)
model.eval()


# ==== Input format ====
class RequirementPair(BaseModel):
    source_text: str
    target_text: str

class RequirementList(BaseModel):
    requirement_texts: List[str]

@router.post("/dependencies/predict")
def predict_dependency(pair: RequirementPair):
    try:
        input_pair = f"{pair.source_text} </s> {pair.target_text}"
        encoded = tokenizer(input_pair, return_tensors="pt", truncation=True, padding=True)

        with torch.no_grad():
            logits = model(**encoded).logits  # shape: [1, 2]
            probs = F.softmax(logits, dim=1)
            depends_on_prob = probs[0][1].item()  # Probability of class 1 (depends)

        return {
            "depends_on": bool(depends_on_prob > 0.5),
            "confidence": round(depends_on_prob, 4)
        }

    except Exception as e:
        return {"error": str(e)}
    

@router.post("/dependencies/batch")
def batch_dependency_analysis(payload: RequirementList):
    try:
        requirements = payload.requirement_texts
        all_results = []

        # Step 1: Predict all pairwise dependencies
        for i, source in enumerate(requirements):
            for j, target in enumerate(requirements):
                if i == j:
                    continue

                input_pair = f"{source} </s> {target}"
                encoded = tokenizer(input_pair, return_tensors="pt", truncation=True, padding=True)

                with torch.no_grad():
                    logits = model(**encoded).logits
                    probs = F.softmax(logits, dim=1)
                    depends_prob = probs[0][1].item()

                all_results.append({
                    "source_id": i,
                    "target_id": j,
                    "source_text": source,
                    "target_text": target,
                    "confidence": round(depends_prob, 4)
                })

        # Step 2: Compute 95th percentile threshold
        confidences = [r["confidence"] for r in all_results]
        threshold = np.percentile(confidences, 99)

        # Step 3: Filter only prominent dependencies
        prominent = [r for r in all_results if r["confidence"] >= threshold]
        for r in prominent:
            r["depends_on"] = True

        return prominent

    except Exception as e:
        return {"error": str(e)}

@router.get("/dependencies/infer")
async def prioritize():
	return {"message": "Dependency endpoint is working."}