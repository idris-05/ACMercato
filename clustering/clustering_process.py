"""Team clustering pipeline for the freezed_dataset.csv file.

This script engineers team-level features, runs K-Means clustering,
scores multiple k values with silhouette, and saves cluster outputs.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable, List, Tuple

import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler


def load_dataset(path: Path) -> pd.DataFrame:
	if not path.exists():
		raise FileNotFoundError(f"Dataset not found at {path}")
	df = pd.read_csv(path)
	if df.empty:
		raise ValueError("Dataset is empty")
	return df


def _proportion_table(df: pd.DataFrame, group_col: str, feature_col: str, top_n: int | None = None) -> pd.DataFrame:
	"""Return normalized counts per group for a categorical column.

	top_n limits the number of categories kept (others are dropped) to avoid
	extremely wide matrices when the cardinality is large.
	"""

	if top_n is not None:
		top_categories = df[feature_col].value_counts().nlargest(top_n).index
		df = df[df[feature_col].isin(top_categories)]

	table = (
		df.groupby(group_col)[feature_col]
		.value_counts(normalize=True)
		.unstack(fill_value=0)
	)
	table.columns = [f"{feature_col}__{c}" for c in table.columns]
	return table


def build_team_features(df: pd.DataFrame) -> pd.DataFrame:
	df = df.copy()
	num_cols = ["market_val_amnt", "transfer_fee_amnt"]
	df[num_cols] = df[num_cols].fillna(df[num_cols].median())
	df["is_free"] = df["is_free"].astype(int)

	grouped = df.groupby("team_name")
	base = grouped.agg(
		total_transfers=("team_name", "size"),
		mean_market_val=("market_val_amnt", "mean"),
		median_market_val=("market_val_amnt", "median"),
		mean_fee=("transfer_fee_amnt", "mean"),
		median_fee=("transfer_fee_amnt", "median"),
		pct_free=("is_free", "mean"),
		unique_seasons=("season", pd.Series.nunique),
	)

	cat_cols: List[Tuple[str, int | None]] = [
		("player_pos_grouped", None),
		("player_region", None),
		("age_group", None),
		("transfer_fee_group", None),
		("window", None),
		# Limit player_nation to keep matrix manageable.
		("player_nation", 15),
	]

	for col, top_n in cat_cols:
		base = base.join(_proportion_table(df, "team_name", col, top_n), how="left")

	base = base.fillna(0)
	return base


def evaluate_kmeans(features: pd.DataFrame, k_values: Iterable[int]) -> pd.DataFrame:
	scaler = StandardScaler()
	X = scaler.fit_transform(features)

	records = []
	for k in k_values:
		model = KMeans(n_clusters=k, n_init="auto", random_state=42)
		labels = model.fit_predict(X)
		score = silhouette_score(X, labels)
		records.append({"k": k, "silhouette": score})

	return pd.DataFrame(records).sort_values("silhouette", ascending=False)


def fit_kmeans(features: pd.DataFrame, k: int):
	scaler = StandardScaler()
	X = scaler.fit_transform(features)
	model = KMeans(n_clusters=k, n_init="auto", random_state=42)
	labels = model.fit_predict(X)
	return model, scaler, labels


def summarize_clusters(features: pd.DataFrame, labels) -> pd.DataFrame:
	df = features.copy()
	df["cluster"] = labels
	return df.groupby("cluster").mean().sort_index()


def run(path: Path, out_dir: Path, k: int | None, k_range: Iterable[int]) -> None:
	out_dir.mkdir(parents=True, exist_ok=True)

	df = load_dataset(path)
	team_features = build_team_features(df)

	score_table = evaluate_kmeans(team_features, k_range)
	best_k = k if k is not None else int(score_table.iloc[0]["k"])

	model, scaler, labels = fit_kmeans(team_features, best_k)
	clusters = pd.DataFrame(
		{
			"team_name": team_features.index,
			"cluster": labels,
		}
	).sort_values(["cluster", "team_name"])

	cluster_profile = summarize_clusters(team_features, labels)

	df_with_cluster = df.merge(clusters, on="team_name", how="left")

	score_table.to_csv(out_dir / "silhouette_scores.csv", index=False)
	clusters.to_csv(out_dir / "team_clusters.csv", index=False)
	cluster_profile.to_csv(out_dir / "cluster_feature_means.csv")
	df_with_cluster.to_csv(out_dir / "dataset_with_clusters.csv", index=False)

	print(f"Tested k values saved to {out_dir/'silhouette_scores.csv'}")
	print(f"Team assignments saved to {out_dir/'team_clusters.csv'}")
	print(f"Cluster feature means saved to {out_dir/'cluster_feature_means.csv'}")
	print(f"Full dataset with clusters saved to {out_dir/'dataset_with_clusters.csv'}")
	print("Top silhouette scores:\n", score_table.head())
	print(f"Chosen k={best_k} with silhouette={score_table[score_table.k==best_k].iloc[0].silhouette:.3f}")


def parse_args() -> argparse.Namespace:
	parser = argparse.ArgumentParser(description="Cluster teams in freezed_dataset.csv")
	parser.add_argument(
		"--dataset",
		type=Path,
		default=Path("freezed_dataset.csv"),
		help="Path to the dataset CSV",
	)
	parser.add_argument(
		"--out",
		type=Path,
		default=Path("outputs"),
		help="Directory to write outputs",
	)
	parser.add_argument(
		"--k",
		type=int,
		default=None,
		help="Force a specific k (otherwise best silhouette is used)",
	)
	parser.add_argument(
		"--k-min",
		type=int,
		default=3,
		help="Minimum k to test",
	)
	parser.add_argument(
		"--k-max",
		type=int,
		default=10,
		help="Maximum k to test",
	)
	return parser.parse_args()


def main() -> None:
	args = parse_args()
	k_range = range(args.k_min, args.k_max + 1)
	run(args.dataset, args.out, args.k, k_range)


if __name__ == "__main__":
	main()
