provider "google" {
  project = var.project_id
  region  = var.region
}

# Create GCS bucket for data lake
resource "google_storage_bucket" "data_lake_bucket" {
  name     = "${var.project_id}-data-lake"
  location = var.region
  
  # Optional settings
  force_destroy               = true
  uniform_bucket_level_access = true
  
  lifecycle_rule {
    action {
      type = "Delete"
    }
    condition {
      age = 30  # days
    }
  }
}

# Create BigQuery dataset
resource "google_bigquery_dataset" "apartment_data" {
  dataset_id                  = "caucasus_apartments"
  friendly_name               = "Caucasus Apartments"
  description                 = "Dataset containing apartment data from Caucasus countries"
  location                    = var.region
  
  delete_contents_on_destroy = true
}

# Create BigQuery tables
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
    "name": "date",
    "type": "DATE",
    "mode": "NULLABLE",
    "description": "Listing date"
  },
  {
    "name": "price_per_sqm",
    "type": "FLOAT",
    "mode": "NULLABLE",
    "description": "Price per square meter"
  }
]
EOF
}