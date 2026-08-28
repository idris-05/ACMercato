# Data dictionary

The published dataset is
[`data/processed/dataset_with_clusters.csv`](../data/processed/dataset_with_clusters.csv).
Each row represents one permanent incoming transfer from the seven leagues in
the upstream data, covering seasons 2009-2021.

## Final clustered columns

| Column | Meaning |
| --- | --- |
| `league` | Upstream league code: `GB1`, `ES1`, `IT1`, `L1`, `FR1`, `PO1`, or `NL1` |
| `season` | Season year |
| `window` | Transfer window: `s` (summer) or `w` (winter) |
| `player_pos_grouped` | Position group: Goalkeeper, Defender, Midfielder, or Forward |
| `player_region` | Nationality region: Western Europe, Eastern Europe, South America, Africa, or Other |
| `age_group` | Career stage: Young (≤21), Prime (22-25), Experienced (26-29), or Veteran (30+) |
| `is_free` | Whether the transfer is marked as free: `True` or `False` |
| `market_val_amnt` | Recorded player market value in EUR |
| `transfer_fee_amnt` | Recorded transfer fee in EUR |
| `team_name` | Acquiring team |
| `player_nation` | Player nationality |
| `transfer_fee_group` | Fee band: Free, Cheap (0-2M), Medium (2-7M), or Expensive (7M+) |
| `cluster` | Team-level K-Means cluster label; nominal category, not ranked |

## Dataset notes

- The final clustered artifact has 17,962 rows and 13 columns.
- The dataset contains only incoming permanent transfers; `is_loan` and `dir`
  are therefore not retained as columns.
- `cluster` was added during the later clustering stage and identifies groups of
  teams with similar transfer-market profiles.
- `age_group` is the final categorical version used in the published artifact.
- Detailed preprocessing decisions are documented in
  [`preprocessing.md`](preprocessing.md). Missing-value treatment is described in
  [`imputation.md`](imputation.md). The clustering logic is described in
  [`clustering.md`](clustering.md).
