"""
Feature Engineering — Encode movie content features for recommendation models.
- Text: Sentence-BERT (all-MiniLM-L6-v2) → 384-dim embeddings
- Image: ResNet-50 → 2048-dim features (optional, needs poster URLs)
- Genre: Multi-hot encoding → 18-dim vectors
All saved as .npy files in data/processed/
"""
import os, json, numpy as np, pandas as pd

RAW_DIR = os.path.join(os.path.dirname(__file__), "raw")
PROCESSED_DIR = os.path.join(os.path.dirname(__file__), "processed")
os.makedirs(PROCESSED_DIR, exist_ok=True)

GENRE_LIST = [
    "Action", "Adventure", "Animation", "Children", "Comedy", "Crime",
    "Documentary", "Drama", "Fantasy", "Film-Noir", "Horror", "Musical",
    "Mystery", "Romance", "Sci-Fi", "Thriller", "War", "Western"
]
NUM_GENRES = len(GENRE_LIST)


def load_enriched_movies():
    """Load enriched movie metadata."""
    path = os.path.join(PROCESSED_DIR, "movies_enriched.json")
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"{path} not found. Run enrich_tmdb.py first."
        )
    with open(path, "r", encoding="utf-8") as f:
        movies = json.load(f)
    return sorted(movies, key=lambda x: x["id"])


def encode_texts(overviews, item_ids):
    """Encode movie overviews using Sentence-BERT all-MiniLM-L6-v2 → 384-dim."""
    from sentence_transformers import SentenceTransformer

    model = SentenceTransformer("all-MiniLM-L6-v2")

    valid_idx = [i for i, t in enumerate(overviews) if t and len(t.strip()) > 10]
    valid_texts = [overviews[i] for i in valid_idx]

    if not valid_texts:
        print("No valid overviews found. Creating zero embeddings.")
        result = np.zeros((len(overviews), 384), dtype=np.float32)
    else:
        print(f"Encoding {len(valid_texts)} overviews with Sentence-BERT...")
        embeddings = model.encode(valid_texts, show_progress_bar=True, batch_size=128)
        result = np.zeros((len(overviews), embeddings.shape[1]), dtype=np.float32)
        for j, idx in enumerate(valid_idx):
            result[idx] = embeddings[j]

    out_path = os.path.join(PROCESSED_DIR, "text_embeddings.npy")
    np.save(out_path, result)
    print(f"Text embeddings saved: {result.shape} → {out_path}")
    return result


def encode_genres(genre_strings):
    """Multi-hot encode genre strings → 18-dim vectors."""
    result = np.zeros((len(genre_strings), NUM_GENRES), dtype=np.float32)
    for i, gs in enumerate(genre_strings):
        if pd.isna(gs) or not gs:
            continue
        for g in gs.split("|"):
            g = g.strip()
            if g in GENRE_LIST:
                result[i, GENRE_LIST.index(g)] = 1.0

    out_path = os.path.join(PROCESSED_DIR, "genre_vectors.npy")
    np.save(out_path, result)
    print(f"Genre vectors saved: {result.shape} → {out_path}")
    return result


def encode_images(poster_urls, item_ids):
    """Extract ResNet-50 features from poster images → 2048-dim."""
    import torch
    from torchvision import models, transforms
    from PIL import Image
    import requests
    from io import BytesIO

    resnet = models.resnet50(weights=models.ResNet50_Weights.IMAGENET1K_V1)
    resnet = torch.nn.Sequential(*list(resnet.children())[:-1])
    resnet.eval()

    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                              std=[0.229, 0.224, 0.225])
    ])

    num_items = len(item_ids)
    features = np.zeros((num_items, 2048), dtype=np.float32)
    count = 0

    for i, url in enumerate(poster_urls):
        if not url or "http" not in url:
            continue
        try:
            resp = requests.get(url, timeout=10)
            img = Image.open(BytesIO(resp.content)).convert("RGB")
            img_t = transform(img).unsqueeze(0)
            with torch.no_grad():
                feat = resnet(img_t).squeeze().numpy()
            features[i] = feat
            count += 1
            if count % 50 == 0:
                print(f"Encoded {count}/{num_items} images...")
        except Exception:
            continue

    out_path = os.path.join(PROCESSED_DIR, "image_embeddings.npy")
    np.save(out_path, features)
    print(f"Image embeddings saved: {features.shape} ({count}/{num_items} success) → {out_path}")
    return features


def create_id_mapping(movies):
    """Create mapping from MovieLens item_id to 0-based index."""
    id_map = {m["id"]: idx for idx, m in enumerate(movies)}
    out_path = os.path.join(PROCESSED_DIR, "id_map.json")
    with open(out_path, "w") as f:
        json.dump(id_map, f)
    print(f"ID mapping saved: {len(id_map)} items → {out_path}")
    return id_map


def preprocess_all(skip_images=True):
    """Run all feature engineering steps."""
    movies = load_enriched_movies()
    print(f"Loaded {len(movies)} movies.")

    # Create ID mapping
    create_id_mapping(movies)

    # Genre encoding
    encode_genres([m.get("genres", "") for m in movies])

    # Text encoding
    encode_texts([m.get("overview", "") for m in movies],
                 [m["id"] for m in movies])

    # Image encoding (optional — skip unless poster URLs available)
    has_posters = sum(1 for m in movies if m.get("poster_url") and "http" in m.get("poster_url", ""))
    if skip_images or has_posters == 0:
        print("Skipping image encoding (no poster URLs or skip_images=True).")
        np.save(
            os.path.join(PROCESSED_DIR, "image_embeddings.npy"),
            np.zeros((len(movies), 2048), dtype=np.float32)
        )
        print("Created zero image embeddings placeholder.")
    else:
        print(f"Encoding {has_posters} poster images with ResNet-50...")
        encode_images([m.get("poster_url", "") for m in movies],
                      [m["id"] for m in movies])

    print("\n=== Feature engineering complete ===")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--images", action="store_true", help="Also encode poster images (slow)")
    args = parser.parse_args()
    preprocess_all(skip_images=not args.images)
