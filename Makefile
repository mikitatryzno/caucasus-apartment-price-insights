.PHONY: download-data build up down run-pipeline run-processing run-dbt terraform-init terraform-apply terraform-destroy

# Download the datasets
download-data:
	python data/download_data.py

# Build Docker images
build:
	docker-compose build

# Start all services
up:
	docker-compose up -d

# Stop all services
down:
	docker-compose down

# Run the full pipeline
run-pipeline:
	docker-compose exec kestra kestra flow run caucasus-apartments apartment-data-loading

# Run only the data processing
run-processing:
	docker-compose exec kestra kestra flow run caucasus-apartments apartment-data-processing

# Run dbt transformations
run-dbt:
	docker-compose run --rm dbt dbt run

# Initialize Terraform
terraform-init:
	cd terraform && terraform init

# Apply Terraform configuration
terraform-apply:
	cd terraform && terraform apply

# Destroy Terraform resources
terraform-destroy:
	cd terraform && terraform destroy