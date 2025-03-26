{{ config(
    materialized='table',
    partition_by={
      "field": "date",
      "data_type": "date",
      "granularity": "month"
    },
    cluster_by=["city", "building_type"]
) }}

SELECT
  city,
  country,
  building_type,
  DATE_TRUNC(date, MONTH) as date,
  COUNT(*) as listing_count,
  AVG(price) as avg_price,
  AVG(price_per_sqm) as avg_price_per_sqm,
  AVG(area) as avg_area,
  AVG(rooms) as avg_rooms,
  -- Floor statistics
  AVG(floor) as avg_floor,
  -- Price premium for new vs old construction
  AVG(CASE WHEN building_type = 'New construction' THEN price_per_sqm END) / 
    NULLIF(AVG(CASE WHEN building_type = 'Old construction' THEN price_per_sqm END), 0) as new_vs_old_premium
FROM {{ ref('stg_apartment_prices') }}
GROUP BY 1, 2, 3, 4
ORDER BY 1, 3, 4