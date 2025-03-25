{{ config(
    materialized='table',
    partition_by={
      "field": "date",
      "data_type": "date",
      "granularity": "month"
    },
    cluster_by=["city", "rooms"]
) }}

SELECT
  city,
  rooms,
  DATE_TRUNC(date, MONTH) as date,
  COUNT(*) as listing_count,
  AVG(price) as avg_price,
  AVG(price_per_sqm) as avg_price_per_sqm,
  AVG(area) as avg_area
FROM {{ ref('stg_apartment_prices') }}
WHERE rooms BETWEEN 1 AND 5
GROUP BY 1, 2, 3
ORDER BY 1, 2, 3