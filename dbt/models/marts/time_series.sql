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
  DATE_TRUNC(date, MONTH) as date,
  AVG(price) as avg_price,
  AVG(price_per_sqm) as avg_price_per_sqm,
  COUNT(*) as listing_count,
  AVG(CASE WHEN rooms = 1 THEN price END) as avg_price_1_room,
  AVG(CASE WHEN rooms = 2 THEN price END) as avg_price_2_rooms,
  AVG(CASE WHEN rooms = 3 THEN price END) as avg_price_3_rooms,
  AVG(CASE WHEN rooms > 3 THEN price END) as avg_price_4plus_rooms
FROM {{ ref('stg_apartment_prices') }}
GROUP BY 1, 2
ORDER BY 1, 2