import os, zipfile, requests, pandas as pd
RAW_DIR = os.path.join(os.path.dirname(__file__), "raw")
os.makedirs(RAW_DIR, exist_ok=True)

def download_movielens_100k():
    """Download MovieLens 100K dataset and extract u.data"""
    url = "https://files.grouplens.org/datasets/movielens/ml-100k.zip"
    zip_path = os.path.join(RAW_DIR, "ml-100k.zip")
    if not os.path.exists(zip_path):
        print(f"Downloading {url}...")
        r = requests.get(url, stream=True)
        r.raise_for_status()
        with open(zip_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
        print("Download complete.")
    if not os.path.exists(os.path.join(RAW_DIR, "ml-100k")):
        with zipfile.ZipFile(zip_path, "r") as z:
            z.extractall(RAW_DIR)
        print("Extracted.")
    return pd.read_csv(
        os.path.join(RAW_DIR, "ml-100k", "u.data"), sep="\t",
        names=["user_id", "item_id", "rating", "timestamp"]
    )

if __name__ == "__main__":
    df = download_movielens_100k()
    print(f"Loaded {len(df)} ratings from {df['user_id'].nunique()} users, {df['item_id'].nunique()} movies")
    csv_path = os.path.join(RAW_DIR, "ratings.csv")
    df.to_csv(csv_path, index=False)
    print(f"Saved to {csv_path}")