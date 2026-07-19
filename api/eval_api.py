"""Evaluation results endpoints."""
import os, json
from fastapi import APIRouter
from db.database import get_connection

router = APIRouter()

PROCESSED_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "processed")
DOCS_DIR = os.path.join(os.path.dirname(__file__), "..", "docs")


@router.get("/results")
async def get_eval_results():
    """Get offline evaluation results for all models."""
    path = os.path.join(PROCESSED_DIR, "eval_results.json")
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    # Return placeholder results
    return {
        "UserCF": {"HR@10": 0.38, "NDCG@10": 0.22, "Recall@10": 0.22, "train_time": 2.5},
        "ItemCF": {"HR@10": 0.42, "NDCG@10": 0.25, "Recall@10": 0.25, "train_time": 3.1},
        "SVD": {"HR@10": 0.45, "NDCG@10": 0.27, "Recall@10": 0.28, "train_time": 1.8},
        "NeuMF": {"HR@10": 0.48, "NDCG@10": 0.30, "Recall@10": 0.30, "train_time": 15.3},
        "MultiModalNCF": {"HR@10": 0.52, "NDCG@10": 0.32, "Recall@10": 0.33, "train_time": 22.7},
        "_note": "Placeholder results. Run train_all.py for actual evaluation."
    }


@router.get("/ablation")
async def get_ablation_results():
    """Get ablation study results for MultiModalNCF."""
    path = os.path.join(PROCESSED_DIR, "ablation_results.json")
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return {
        "Full Model": {"HR@10": 0.52, "NDCG@10": 0.28},
        "w/o Text": {"HR@10": 0.49, "NDCG@10": 0.26},
        "w/o Image": {"HR@10": 0.50, "NDCG@10": 0.26},
        "w/o Genre": {"HR@10": 0.51, "NDCG@10": 0.27},
        "w/o GMF": {"HR@10": 0.47, "NDCG@10": 0.24},
        "w/o Content": {"HR@10": 0.45, "NDCG@10": 0.23},
        "_note": "Expected results. Run ablation experiment for actual data."
    }
