# Football Transfers: Analysis-Ready Dataset

This repository documents a reproducible preprocessing and clustering pipeline for football
transfer records from seven major European leagues between 2009 and 2021, used as the basis
for a Multiple Correspondence Analysis (MCA) of transfer-market acquisition profiles
(see `docs/report[FR].pdf`).

## Provenance

The raw starting point is the upstream `transfers.csv` file from
[d2ski/football-transfers-data](https://github.com/d2ski/football-transfers-data).
The copy used here is stored in [`data/raw/raw_transfers.csv`](data/raw/raw_transfers.csv).
The upstream dataset was scraped from Transfermarkt; see the original project
README for the source details.

## Full pipeline from raw data to published result

The repository follows a staged workflow:

1. Raw external dataset ingestion
   - The source file contains 70,006 transfer records.
   - We keep the original Transfermarkt schema initially and then progressively
     filter it down to the analysis scope.

2. Cleaning and filtering
   - Remove non-transfer events such as `is_loan_end` and `is_retired`.
   - Remove impossible values above the EUR 250 million cap used in the project.
   - Keep only permanent incoming transfers (`is_loan == False` and `dir == "in"`).
   - Drop rows with missing `player_age` or `player_nation`.
   - This reduces the dataset from 70,006 raw rows to 17,962 final rows.

3. Derived categorical variables
   - `player_pos_grouped`: original detailed positions are merged into four broad roles:
     Goalkeeper, Defender, Midfielder, and Forward.
   - `player_region`: player nationalities are grouped into Western Europe,
     Eastern Europe, South America, Africa, and Other.
   - `age_group`: continuous age is converted into football-relevant stages.
     In the published artifact, the final bins are:
     `Young (≤21)`, `Prime (22-25)`, `Experienced (26-29)`, and `Veteran (30+)`.
   - `transfer_fee_group`: final fee bands are created after the clustering stage:
     `Free`, `Cheap (0-2M)`, `Medium (2-7M)`, and `Expensive (7M+)`.

4. Final stored analysis artifact
   - The final published file is
     [`data/processed/dataset_with_clusters.csv`](data/processed/dataset_with_clusters.csv).
   - This file contains 17,962 transfers and 13 columns, including the derived
     `transfer_fee_group` and team-level `cluster` feature.
   - The preprocessing script creates an intermediate base table in `outputs/`.
     The clustering-stage variables are added later and saved in `data/processed/`.

## Project report and technical materials

The main written project report is available in
[docs/report[FR].pdf](docs/report%5BFR%5D.pdf).

The repository also includes the technical and methodological material used to
construct the final dataset:

- [docs/preprocessing.md](docs/preprocessing.md): cleaning and feature-engineering workflow
- [docs/imputation.md](docs/imputation.md): missing-value imputation strategy
- [docs/clustering.md](docs/clustering.md): clustering logic and interpretation
- [docs/data_dictionary.md](docs/data_dictionary.md): final dataset schema
- [clustering/README.md](clustering/README.md): clustering-specific resources
- [model/README.md](model/README.md): imputation/modeling resources

## Documentation and project structure

```text
data/
  raw/raw_transfers.csv
  processed/dataset_with_clusters.csv

docs/
  report[FR].pdf
  preprocessing.md
  imputation.md
  clustering.md
  data_dictionary.md

notebooks/
  preprocessing.ipynb
  mca_analysis.ipynb

src/
  preprocess.py

clustering/
  README.md
  clustering_process.py

model/
  README.md
  model.ipynb
```

The repository keeps the raw source file and the final analysis dataset in
`data/`, while the `clustering/` and `model/` folders focus on the code logic
used to generate those stages. Intermediate tables are not duplicated here.

## Reproduce the processed dataset

```bash
python -m pip install -r requirements.txt
python src/preprocess.py
```

The project keeps the final clustered dataset as the authoritative published
artifact. The intermediate base table is reproducible from the script, while the
clustering columns (`transfer_fee_group`, `cluster`) are added in the later
analysis stage.

## Notes on documentation and interpretation

- The final published CSV is the version used in the report and the clustering
  analysis, this is the source of truth for category definitions and counts.
- The notebooks include the preprocessing walkthrough and the executed MCA
  analysis. `mca_analysis.ipynb` is the single published analysis notebook. Its
  saved outputs were preserved while its explanatory setup text and repository
  data path were cleaned, it was not re-executed during preparation.

## License

The preprocessing code and documentation are released under the MIT License.
The raw data remains attributable to its upstream source and to Transfermarkt.
