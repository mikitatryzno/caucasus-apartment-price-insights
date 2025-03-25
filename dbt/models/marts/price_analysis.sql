{{ config(
    materialized='table',
    partition_by={
      "field": "date",
      "data_type": "date",
      "granularity": "month"
    },
    cluster_by=["city", "neighborhood"]
) }}

WITH price_stats AS (
  SELECT
    city,
    neighborhood,
    DATE_TRUNC(date, MONTH) as month,
    AVG(price) as avg_price,
    AVG(price_per_sqm) as avg_price_per_sqm,
    COUNT(*) as listing_count
  FROM {{ ref('stg_apartment_prices') }}
  GROUP BY 1, 2, 3
)

SELECT
  city,
  neighborhood,
  month as date,
  avg_price,
  avg_price_per_sqm,
  listing_count,
  LAG(avg_price) OVER (PARTITION BY city, neighborhood ORDER BY month) as prev_month_avg_price,
  (avg_price - LAG(avg_price) OVER (PARTITION BY city, neighborhood ORDER BY month)) / 
    NULLIF(LAG(avg_price) OVER (PARTITION BY city, neighborhood ORDER BY month), 0) * 100 as price_change_pct
FROM price_stats