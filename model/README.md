# Imputation and modeling workflow

This folder contains the code and notebook used for the missing-value imputation
and modeling stage of the project.

The repository keeps the raw source dataset and the final output dataset in the
main `data/` folders. This folder is intentionally limited to the modeling logic
itself and does not duplicate intermediate data files.

## Included technical files

- `model.ipynb`: full modeling and imputation workflow, including preprocessing,
  model comparison, validation, and output generation.

## Notes

The methodology is summarized in [`../docs/imputation.md`](../docs/imputation.md).
This folder shows the actual modeling logic used during the imputation process;
the input and final dataset are stored in the repository data directories instead
of being duplicated here.
