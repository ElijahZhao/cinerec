"""
Offline Evaluation Runner — Train and evaluate all 5 models on MovieLens 100K.
Uses Leave-One-Out split: each user's last interaction as test, rest as train.
Evaluates HR@K, NDCG@K, Recall@K at K={5, 10, 20}.
Saves results to evaluation/results.json.
"""
import os, sys, json, time, numpy as np, pandas as pd

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from models.user_cf import UserCF
from models.item_cf import ItemCF
from models.svd_als import SVDALS
from models.neumf import NeuMF
from models.multimodal_ncf import MultiModalNCF
from evaluation.metrics import evaluate_model

RAW_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "processed")


def load_data():
    """Load MovieLens ratings and build train/test split."""
    csv_path = os.path.join(RAW_DIR, "ratings.csv")
    df = pd.read_csv(csv_path)

    # Sort by timestamp for Leave-One-Out
    df = df.sort_values("timestamp").reset_index(drop=True)

    # Last interaction per user = test
    test_df = df.groupby("user_id").last().reset_index()
    train_df = df.drop(test_df.index)

    # Build numpy arrays
    train_data = {
        "user_id": train_df["user_id"].values,
        "item_id": train_df["item_id"].values,
        "rating": train_df["rating"].values,
    }

    # Test pairs: (user_id, {relevant_item_ids})
    test_pairs = []
    for _, row in test_df.iterrows():
        test_pairs.append((int(row["user_id"]), {int(row["item_id"])}))

    print(f"Data: {len(train_df)} train, {len(test_df)} test")
    print(f"Users: {df['user_id'].nunique()}, Items: {df['item_id'].nunique()}")

    return train_data, test_pairs, df


def run_evaluation():
    """Train all models and evaluate."""
    train_data, test_pairs, full_df = load_data()
    k_values = [5, 10, 20]
    all_results = {}

    models_to_train = [
        ("UserCF", lambda: UserCF(k=50)),
        ("ItemCF", lambda: ItemCF(k=50)),
        ("SVD", lambda: SVDALS(k=64, lambda_reg=0.01)),
        ("NeuMF", lambda: NeuMF(embedding_dim=32, mlp_dims=(128, 64, 32), epochs=10, batch_size=512)),
        ("MultiModalNCF", lambda: MultiModalNCF(embedding_dim=32, mlp_dims=(128, 64, 32), epochs=10, batch_size=512)),
    ]

    for name, model_factory in models_to_train:
        print(f"\n{'='*60}")
        print(f"Training {name}...")
        print(f"{'='*60}")

        model = model_factory()
        start_time = time.time()

        try:
            model.fit(train_data)
            train_time = time.time() - start_time

            print(f"Evaluating {name}...")
            results = evaluate_model(model, test_pairs, k_values=k_values)
            results["train_time"] = round(train_time, 2)

            # Print results
            print(f"\n{name} Results:")
            for metric, value in sorted(results.items()):
                if metric != "train_time":
                    print(f"  {metric}: {value:.4f}")
                else:
                    print(f"  {metric}: {value}s")

            all_results[name] = results

        except Exception as e:
            print(f"ERROR training {name}: {e}")
            import traceback
            traceback.print_exc()
            all_results[name] = {"error": str(e)}

    # Save results
    results_path = os.path.join(RESULTS_DIR, "eval_results.json")
    with open(results_path, "w") as f:
        json.dump(all_results, f, indent=2)
    print(f"\nResults saved to {results_path}")

    return all_results


if __name__ == "__main__":
    run_evaluation()