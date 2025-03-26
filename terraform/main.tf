# Update only the schema part of the BigQuery table resource
resource "google_bigquery_table" "apartment_prices" {
  dataset_id = google_bigquery_dataset.apartment_data.dataset_id
  table_id   = "apartment_prices"
  
  time_partitioning {
    type  = "DAY"
    field = "date"
  }
  
  clustering = ["city", "neighborhood"]
  
  schema = <<EOF
[
  {
    "name": "id",
    "type": "STRING",
    "mode": "NULLABLE",
    "description": "Unique identifier"
  },
  {
    "name": "original_price",
    "type": "FLOAT",
    "mode": "NULLABLE",
    "description": "Original price in local currency"
  },
  {
    "name": "original_currency",
    "type": "STRING",
    "mode": "NULLABLE",
    "description": "Original currency (GEL, USD, AZM)"
  },
  {
    "name": "price",
    "type": "FLOAT",
    "mode": "NULLABLE",
    "description": "Price in USD"
  },
  {
    "name": "area",
    "type": "FLOAT",
    "mode": "NULLABLE",
    "description": "Area in square meters"
  },
  {
    "name": "rooms",
    "type": "INTEGER",
    "mode": "NULLABLE",
    "description": "Number of rooms"
  },
  {
    "name": "city",
    "type": "STRING",
    "mode": "REQUIRED",
    "description": "City name"
  },
  {
    "name": "neighborhood",
    "type": "STRING",
    "mode": "NULLABLE",
    "description": "Neighborhood name"
  },
  {
    "name": "price_per_sqm",
    "type": "FLOAT",
    "mode": "NULLABLE",
    "description": "Price per square meter in USD"
  },
  {
    "name": "floor",
    "type": "INTEGER",
    "mode": "NULLABLE",
    "description": "Floor number"
  },
  {
    "name": "building_type",
    "type": "STRING",
    "mode": "NULLABLE",
    "description": "Type of building (New construction, Old construction, Under construction)"
  },
  {
    "name": "date",
    "type": "DATE",
    "mode": "NULLABLE",
    "description": "Listing date"
  }
]
EOF
}