{{ config(
    materialized='view'
) }}

SELECT
    id,
    price,
    area,
    rooms,
    city,
    neighborhood,
    date,
    price_per_sqm
FROM
    {{ source('raw', 'apartment_prices') }}