"""Build the intermediate football transfer dataset before clustering."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


POSITION_MAPPING = {
    "GK": "Goalkeeper",
    "CB": "Defender",
    "LB": "Defender",
    "RB": "Defender",
    "defence": "Defender",
    "DM": "Midfielder",
    "CM": "Midfielder",
    "AM": "Midfielder",
    "LM": "Midfielder",
    "RM": "Midfielder",
    "midfield": "Midfielder",
    "LW": "Forward",
    "RW": "Forward",
    "CF": "Forward",
    "SS": "Forward",
    "attack": "Forward",
}

WESTERN_EUROPE = {
    "England", "France", "Germany", "Italy", "Spain", "Netherlands",
    "Belgium", "Portugal", "Scotland", "Switzerland", "Austria", "Denmark",
    "Sweden", "Norway", "Finland", "Ireland", "Wales", "Iceland", "Cyprus",
    "Malta", "Luxembourg", "Liechtenstein", "Jersey", "Northern Ireland",
}
EASTERN_EUROPE = {
    "Poland", "Czech Republic", "Russia", "Ukraine", "Croatia", "Serbia",
    "Romania", "Slovakia", "Slovenia", "Bosnia-Herzegovina", "Bulgaria",
    "Hungary", "Albania", "North Macedonia", "Greece", "Belarus", "Kosovo",
    "Montenegro", "Georgia", "Armenia", "Moldova", "Kazakhstan", "Turkey",
    "Estonia", "Latvia", "Lithuania",
}
SOUTH_AMERICA = {
    "Brazil", "Argentina", "Uruguay", "Colombia", "Chile", "Paraguay",
    "Ecuador", "Peru", "Venezuela", "Bolivia", "French Guiana", "Guyana",
    "Suriname",
}
AFRICA = {
    "Senegal", "Ghana", "Nigeria", "Ivory Coast", "Cameroon", "Morocco",
    "Algeria", "Tunisia", "Mali", "Egypt", "Burkina Faso", "Guinea",
    "South Africa", "DR Congo", "Congo", "Angola", "Gabon", "Togo", "Benin",
    "Cape Verde Islands", "Zambia", "Zimbabwe", "Madagascar", "Mauritius",
    "Mauritania", "Somalia", "Sierra Leone", "Rwanda", "Uganda", "Libya",
    "Eritrea", "Burundi", "Comoros", "Sao Tome and Principe", "The Gambia",
}


def region_for(nation: str) -> str:
    if nation in WESTERN_EUROPE:
        return "Western Europe"
    if nation in EASTERN_EUROPE:
        return "Eastern Europe"
    if nation in SOUTH_AMERICA:
        return "South America"
    if nation in AFRICA:
        return "Africa"
    return "Other"


def build_dataset(input_path: Path, output_path: Path) -> pd.DataFrame:
    """Apply documented filters and transformations before later clustering."""
    df = pd.read_csv(input_path)
    df = df.loc[~(df["is_loan_end"] | df["is_retired"])].copy()
    df = df.loc[df["transfer_fee_amnt"].isna() | (df["transfer_fee_amnt"] < 250_000_000)]
    df = df.drop(
        columns=["team_id", "player_id", "counter_team_id", "transfer_id",
                 "player_nation2", "player_name", "is_loan_end", "is_retired"]
    )
    df = df.loc[df["is_loan"].eq(False) & df["dir"].eq("in")]
    df = df.dropna(subset=["player_age", "player_nation"]).copy()
    df["player_pos_grouped"] = df["player_pos"].map(POSITION_MAPPING).fillna("Midfielder")
    df["player_region"] = df["player_nation"].map(region_for)

    # These boundaries match the published artifact used downstream.
    df["age_group"] = pd.cut(
        df["player_age"],
        bins=[0, 21, 25, 29, 100],
        labels=["Young (≤21)", "Prime (22-25)", "Experienced (26-29)", "Veteran (30+)"],
    )
    df = df.drop(columns=["player_age"])
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    return df


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=Path("data/raw/raw_transfers.csv"))
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("outputs/analysis_ready_transfers_base.csv"),
    )
    args = parser.parse_args()
    result = build_dataset(args.input, args.output)
    print(f"Wrote {len(result):,} rows and {len(result.columns)} columns to {args.output}")


if __name__ == "__main__":
    main()
