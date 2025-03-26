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
    country,
    building_type,
    DATE_TRUNC(date, MONTH) as month,
    AVG(price) as avg_price,
    AVG(price_per_sqm) as avg_price_per_sqm,
    COUNT(*) as listing_count,
    AVG(area) as avg_area,
    AVG(rooms) as avg_rooms,
    AVG(floor) as avg_floor
  FROM {{ ref('stg_apartment_prices') }}
  GROUP BY 1, 2, 3, 4, 5
)

SELECT
  city,
  neighborhood,
  country,
  building_type,
  month as date,
  avg_price,
  avg_price_per_sqm,
  listing_count,
  avg_area,
  avg_rooms,
  avg_floor,
  LAG(avg_price) OVER (PARTITION BY city, neighborhood, building_type ORDER BY month) as prev_month_avg_price,
  (avg_price - LAG(avg_price) OVER (PARTITION BY city, neighborhood, building_type ORDER BY month)) / 
    NULLIF(LAG(avg_price) OVER (PARTITION BY city, neighborhood, building_type ORDER BY month), 0) * 100 as price_change_pct
FROM price_stats