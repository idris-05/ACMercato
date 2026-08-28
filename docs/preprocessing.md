# Preprocessing and final artifact

The pipeline in [`src/preprocess.py`](../src/preprocess.py) converts the raw
Transfermarkt export into an intermediate base table in `outputs/`. The final
clustered artifact is stored in `data/processed/dataset_with_clusters.csv` and
contains the clustering-stage columns used in the report.

## 1. Raw source and scope

The upstream source contains 70,006 rows. The project then applies a sequence of
filters to keep only the transfer records relevant to the analysis:

- permanent transfers only,
- incoming transfers only,
- the relevant European leagues and seasons,
- rows with valid core player metadata.

## 2. Step-by-step cleaning pipeline

1. Remove loan-ending and retirement events.
2. Remove transfer-fee values at or above EUR 250 million.
3. Remove identifiers and redundant high-cardinality fields.
4. Keep permanent transfers (`is_loan == False`) arriving at a club
   (`dir == "in"`).
5. Remove rows missing `player_age` or `player_nation`.
6. Group detailed positions into Goalkeeper, Defender, Midfielder, and Forward.
7. Group nationalities into Western Europe, Eastern Europe, South America,
   Africa, and Other.
8. Convert age into football-relevant stages.
9. Save the base result as `outputs/analysis_ready_transfers_base.csv`.
10. In the later clustering stage, add `transfer_fee_group` and `cluster` and
   save the final artifact in `data/processed/`.

The row count follows the intended flow of the project:

- raw dataset: 70,006 rows
- after non-transfer filtering: 55,597 rows
- after fee cap: 55,561 rows
- after permanent incoming transfer filter: 17,968 rows
- after missing-age/nationality validation: 17,962 rows

## 3. Derived categories in the published dataset

### `player_pos_grouped`
- Goalkeeper
- Defender
- Midfielder
- Forward

### `player_region`
- Western Europe
- Eastern Europe
- South America
- Africa
- Other

### `age_group`
- Young (≤21)
- Prime (22-25)
- Experienced (26-29)
- Veteran (30+)

### `transfer_fee_group`
- Free
- Cheap (0-2M)
- Medium (2-7M)
- Expensive (7M+)

## 4. Final artifact

The final processed dataset retained in the repository is
[`../data/processed/dataset_with_clusters.csv`](../data/processed/dataset_with_clusters.csv).
It contains 17,962 rows and 13 columns and is the analysis-ready artifact used
by the project.

Compared with the intermediate base table, it includes two additional derived
columns:

- `transfer_fee_group`
- `cluster`

## 5. Missing-value treatment

The raw and intermediate datasets contain missing financial values:

- `market_val_amnt`: 4,387 missing
- `transfer_fee_amnt`: 5,878 missing

These values were later completed as part of the imputation workflow described in
[`imputation.md`](imputation.md). The final dataset contains no missing values in
those two financial columns.

## 6. Interpretation notes

- A missing transfer fee is not automatically zero: the source may omit a fee
  when it was not disclosed.
- The processed table is focused on incoming acquisition behavior rather than the
  full market-wide transfer activity.
- The repository intentionally separates the base cleaning pipeline from the
  later clustering step, because the final artifact was prepared in a staged
  analysis workflow rather than as a single one-shot transformation.

## 7. Notebook status

The preprocessing notebook contains the full technical implementation of the
filtering and transformation work. The documentation in this repository is the
cleaned, publication-oriented summary of that workflow.
