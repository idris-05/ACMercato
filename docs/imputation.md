# Missing-value imputation workflow

This document describes the missing-value treatment used before the final
clustered analysis dataset was produced.

## Why the financial columns needed imputation

The raw transfer dataset contains missing values in the financial fields used for
analysis:

- `market_val_amnt`
- `transfer_fee_amnt`

These values are not random noise: they reflect real reporting gaps in the source
market data. For example, some transfers do not report a fee at all, and some
player valuations are absent from the upstream records.

The project therefore treats the missingness as part of the real dataset,
while still producing a complete analysis table for the final clustering stage.

## Models considered

During the original project workflow, several regression models were compared for
imputation:

- Linear Regression
- Ridge Regression
- Random Forest Regressor
- Gradient Boosting Regressor

## Selected model

In the notebook execution, the best-performing model was the Random Forest
Regressor, based on the lowest test MAE.

This model was used to complete the missing financial values before the final
clustered artifact was generated.

## Preprocessing used for the model

The project workflow used a standard tabular machine-learning setup for the
imputation step:

- numeric variables were standardized,
- categorical variables were one-hot-encoded,
- model quality was evaluated with MAE, RMSE, R², and cross-validation,
- model comparison was driven by the lowest test MAE, while the other metrics
  were tracked for reference.

This ensured that the imputation step respected the mixed nature of the datasets,
where both continuous and categorical predictors were present.

## Final result

The final clustered artifact contains no missing values in either financial
column. The imputed values are therefore part of the published analysis table,
but the exact model-training implementation itself is not re-created in this
repository.

## Important interpretation note

The imputation step was part of the analysis preparation, not a change to the
underlying transfer market data. It is used to complete the final analysis-ready
matrix while preserving the original downstream dataset structure.
