# Data Quality Report

## Implemented Checks
The following data quality checks were implemented using **Soda Core** in the ingestion pipeline:

1.  **Row Count Check**: `row_count > 0`
    *   Ensures that the dataset is not empty.
2.  **Missing Value Check (id)**: `missing_count(id) = 0`
    *   Ensures that every product has a unique identifier.
3.  **Uniqueness Check (id)**: `duplicate_count(id) = 0`
    *   Ensures that there are no duplicate product IDs.
4.  **Format Validation (price)**: `invalid_count(price) = 0 (valid format: decimal)`
    *   Ensures that the price column contains valid decimal numbers.
5.  **Value Range Check (price)**: `min(price) > 0`
    *   Ensures that no product has a negative or zero price.

## Sample Results
During a typical pipeline run, the results are captured and sent to the Metadata API.

| Check Name | Outcome | Observed Value | Expected Value |
| :--- | :--- | :--- | :--- |
| Row Count | Pass | 5 | row_count > 0 |
| Missing (id) | Pass | 0 | missing_count(id) = 0 |
| Duplicate (id) | Pass | 0 | duplicate_count(id) = 0 |
| Invalid (price) | Pass | 0 | invalid_count(price) = 0 |
| Range (price) | Pass | 2500 | min(price) > 0 |

These results are persisted in the `data_quality_results` table and can be retrieved via the API.
