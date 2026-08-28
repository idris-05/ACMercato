# Clustering workflow

This folder contains the code used to build the final team-level cluster labels
included in the published analysis dataset.

The project keeps only the source data and final processed data in the main data
folder. This folder is intentionally limited to the clustering logic itself, not
intermediate datasets.

The final published output remains in:
[`../data/processed/dataset_with_clusters.csv`](../data/processed/dataset_with_clusters.csv).

## Included technical files

- `clustering_process.py`: team-level clustering implementation using engineered
  features, StandardScaler, and K-Means with silhouette-based k selection.

## Notes

The full methodology is summarized in [`../docs/clustering.md`](../docs/clustering.md).
This folder shows the actual logic used for clustering; the raw input and final
processed output are handled in the repository data folders instead of being
duplicated here.
