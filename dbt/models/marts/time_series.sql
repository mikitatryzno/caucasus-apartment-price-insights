{{ config(
    materialized='table',
    partition_by={
      "field": "date",
      "data_type": "date",
      "granularity": "month"
    },
    cluster_by=["city"]
) }}

SELECT
  city,
  country,
  building_type,
  DATE_TRUNC(date, MONTH) as date,
  AVG(price) as avg_price,
  AVG(price_per_sqm) as avg_price_per_sqm,
  COUNT(*) as listing_count,
  AVG(CASE WHEN rooms = 1 THEN price END) as avg_price_1_room,
  AVG(CASE WHEN rooms = 2 THEN price END) as avg_price_2_rooms,
  AVG(CASE WHEN rooms = 3 THEN price END) as avg_price_3_rooms,
  AVG(CASE WHEN rooms > 3 THEN price END) as avg_price_4plus_rooms,
  -- Floor position analysis
  AVG(CASE WHEN floor_position = 'Ground floor' THEN price_per_sqm END) as avg_price_ground_floor,
  AVG(CASE WHEN floor_position = 'Middle floor' THEN price_per_sqm END) as avg_price_middle_floor,
  AVG(CASE WHEN floor_position = 'High floor' THEN price_per_sqm END) as avg_price_high_floor
FROM {{ ref('stg_apartment_prices') }}
GROUP BY 1, 2, 3, 4
ORDER BY 1, 3, 4