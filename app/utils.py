import os
import pandas as pd
import matplotlib
matplotlib.use("Agg")  # for headless environments (no GUI)
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

ALLOWED = {".csv"}

# ---------- Check if file is CSV ----------
def allowed(fname):
    return os.path.splitext(fname)[1].lower() in ALLOWED

# ---------- K-Means Clustering ----------
def cluster_csv(path, k=5):
    df = pd.read_csv(path)

    # Use only numeric columns
    X = df.select_dtypes(include=["int64", "float64"])
    if X.empty:
        raise ValueError("No numeric columns to cluster")

    # Apply K-Means clustering
    km = KMeans(n_clusters=k, random_state=42)
    df["Cluster"] = km.fit_predict(X)

    # Optional 2D plot
    plot_path = None
    if {"Annual Income (k$)", "Spending Score (1-100)"} <= set(df.columns):
        plt.figure()
        plt.scatter(df["Annual Income (k$)"], df["Spending Score (1-100)"],
                    c=df["Cluster"])
        plt.xlabel("Annual Income (k$)")
        plt.ylabel("Spending Score (1-100)")
        plt.title("Customer Segmentation")
        plot_path = os.path.splitext(path)[0] + "_plot.png"
        plt.savefig(plot_path, dpi=150, bbox_inches="tight")
        plt.close()

    # Save clustered data
    clustered_path = os.path.splitext(path)[0] + "_clustered.csv"
    df.to_csv(clustered_path, index=False)

    # Preview first 10 rows
    preview_html = df.head(10).to_html(classes="table table-sm")

    return clustered_path, plot_path, preview_html
