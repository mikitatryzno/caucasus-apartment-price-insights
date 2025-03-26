{{ config(
    materialized='view'
) }}

SELECT
    id,
    original_price,
    original_currency,
    price,
    area,
    rooms,
    city,
    neighborhood,
    price_per_sqm,
    floor,
    building_type,
    date,
    -- Additional fields
    CASE 
        WHEN city = 'Tbilisi' THEN 'Georgia'
        WHEN city = 'Yerevan' THEN 'Armenia'
        WHEN city = 'Baku' THEN 'Azerbaijan'
        ELSE NULL
    END as country,
    -- Standardized size category
    CASE 
        WHEN area < 50 THEN 'Small'
        WHEN area >= 50 AND area < 100 THEN 'Medium'
        WHEN area >= 100 AND area < 150 THEN 'Large'
        ELSE 'Very Large'
    END as size_category,
    -- Floor position category (simplified without max_floor)
    CASE
        WHEN floor = 1 THEN 'Ground floor'
        WHEN floor > 10 THEN 'High floor'
        WHEN floor > 1 AND floor <= 10 THEN 'Middle floor'
        ELSE 'Unknown'
    END as floor_position
FROM
    {{ source('raw', 'apartment_prices') }}
WHERE
    price > 0 AND area > 0  -- Filter out invalid entries