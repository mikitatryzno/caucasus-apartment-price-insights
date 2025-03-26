# Caucasus Apartment Price Insights

## Project Overview

This project creates an end-to-end data pipeline for analyzing apartment prices across three Caucasus capital cities: Tbilisi (Georgia), Yerevan (Armenia), and Baku (Azerbaijan). The pipeline ingests data from CSV files, processes it using Spark, loads it into BigQuery, and visualizes insights using Looker Studio.

## Problem Statement

The real estate markets in the Caucasus region are evolving rapidly, but there's limited comparative analysis across these neighboring countries. This project aims to create a comprehensive data pipeline and dashboard that provides insights into apartment pricing trends across Tbilisi, Yerevan, and Baku. By analyzing these markets together, stakeholders can identify regional patterns, investment opportunities, and affordability comparisons across the three capital cities.

Key questions this project answers:
1. How do apartment prices compare across the three capital cities?
2. What are the temporal trends in apartment prices in each city?
3. How do apartment characteristics (size, rooms, etc.) affect pricing in different markets?
4. Which areas within each city offer the best value for money?

## Architecture

![Architecture Diagram](docs/architecture.png)

The project uses the following architecture:
1. **Data Sources**: CSV files containing apartment data from the three cities
2. **Data Ingestion**: Kestra orchestrates the download and ingestion of data
3. **Data Lake**: Google Cloud Storage for raw and processed data
4. **Data Processing**: Apache Spark for data cleaning and transformation
5. **Data Warehouse**: BigQuery with optimized table structure
6. **Transformations**: dbt for data modeling and business logic
7. **Dashboard**: Looker Studio for visualization

## Technologies Used

- **Cloud**: Google Cloud Platform (GCP)
- **Infrastructure as Code**: Terraform
- **Workflow Orchestration**: Kestra
- **Data Processing**: Apache Spark
- **Data Warehouse**: BigQuery
- **Transformations**: dbt
- **Visualization**: Looker Studio
- **Containerization**: Docker

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Google Cloud Platform account (for production deployment)
- Kaggle account (for downloading datasets)

### Local Setup

1. Clone the repository:

```bash
git clone https://github.com/yourusername/caucasus-apartment-price-insights.git cd caucasus-apartment-price-insights
```

2. Download the datasets:

```bash
python data/download_data.py
```


3. Set up GCP credentials:
- Create a service account with the necessary permissions (BigQuery Admin, Storage Admin)
- Download the service account key as JSON
- Save it as `dbt/keyfile.json`
- Set the environment variable:
  ```
  export GCP_PROJECT=your-gcp-project-id
  ```

4. Start the local environment:

``bash
docker-compose up -d
``

5. Access the services:
- Kestra UI: http://localhost:8080
- Spark Master UI: http://localhost:8181

### Running the Pipeline

Use the Makefile commands to run different parts of the pipeline:

Download the datasets

```
make download-data
```

Build Docker images

```
make build
```

Start all services

```
make up
```

Run the full pipeline

```
make run-pipeline
```

Run only the data processing

```
make run-processing
```

Run dbt transformations

```
make run-dbt
```

Stop all services

```
make down
```

### Deploying to GCP

1. Initialize Terraform:

```
make terraform-init
```

2. Apply Terraform configuration:

```
make terraform-apply
```

3. When prompted, enter your GCP project ID.


## Project Structure

caucasus-apartment-price-insights/
├── .github/workflows/           # CI/CD configuration (to be added later if needed)
├── terraform/                   # Infrastructure as Code
│   ├── main.tf                  # Main Terraform configuration
│   ├── variables.tf             # Terraform variables
│   └── outputs.tf               # Terraform outputs
├── data/                        # Local data directory
│   └── download_data.py         # Script to download datasets
├── kestra/                      # Kestra workflows
│   └── flows/
│       ├── data_ingestion.yml   # Data ingestion workflow
│       ├── data_processing.yml  # Data processing workflow
│       └── data_loading.yml     # Data loading workflow
├── spark/                       # Spark jobs
│   └── jobs/
│       ├── data_cleaning.py     # Data cleaning job
│       └── data_analysis.py     # Data analysis job
├── dbt/                         # dbt transformations
│   ├── dbt_project.yml          # dbt project configuration
│   ├── profiles.yml             # dbt connection profiles
│   ├── models/
│   │   ├── staging/
│   │   │   ├── stg_apartment_prices.sql
│   │   │   └── sources.yml
│   │   ├── marts/
│   │   │   ├── price_analysis.sql
│   │   │   ├── time_series.sql
│   │   │   └── room_price_comparison.sql
│   │   └── schema.yml           # dbt documentation
│   └── macros/                  # dbt macros (empty for now)
├── docker/                      # Docker configuration
│   ├── kestra/
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   ├── spark/
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   └── dbt/
│       └── Dockerfile
├── docker-compose.yml           # Docker Compose configuration
├── Makefile                     # Makefile for common commands
├── requirements.txt             # Python dependencies
└── README.md                    # Project documentation


## Data Warehouse Design

The BigQuery data warehouse is designed with performance in mind:

- **Partitioning**: Tables are partitioned by date to optimize queries that filter by time periods
- **Clustering**: Tables are clustered by city and neighborhood to optimize queries that filter by location
- **Materialized Views**: dbt creates materialized views for common query patterns

## Dashboard

The final dashboard provides insights into apartment prices across the three cities:

1. **Price Comparison**: Average prices by city and number of rooms
2. **Time Series Analysis**: Price trends over time for each city
3. **Neighborhood Analysis**: Price distribution within each city
4. **Room Count Analysis**: How prices vary by number of rooms

## Explanation of Design Choices

### Why Kestra for Workflow Orchestration?

Kestra was chosen for its robust workflow orchestration capabilities, including:
- Visual workflow editor
- Built-in error handling and retries
- Comprehensive monitoring
- Support for various task types including Python scripts, shell commands, and GCP operations

### Why Spark for Data Processing?

Spark provides:
- Scalable data processing for large datasets
- Rich API for data transformation
- Integration with GCP storage
- Support for both batch and streaming processing

### Why dbt for Transformations?

dbt offers:
- Version-controlled SQL transformations
- Documentation generation
- Testing framework for data quality
- Dependency management between models

### BigQuery Optimization Strategy

The BigQuery tables are optimized by:
- Partitioning by date to improve query performance for time-based analysis
- Clustering by city and neighborhood to speed up location-based filtering
- Using appropriate data types to minimize storage and improve query performance

## Data Pipeline Flow

1. **Data Ingestion**:
   - Kestra workflow `apartment-data-ingestion` reads CSV files
   - Data is uploaded to GCS raw data bucket

2. **Data Processing**:
   - Kestra workflow `apartment-data-processing` triggers Spark jobs
   - Spark cleans and transforms the data
   - Processed data is saved back to GCS

3. **Data Loading**:
   - Kestra workflow `apartment-data-loading` loads processed data to BigQuery
   - Data is appended to the apartment_prices table

4. **Data Transformation**:
   - dbt models transform the raw data into analytical views
   - Staging models clean and standardize the data
   - Mart models create business-level aggregations

5. **Visualization**:
   - Looker Studio connects to BigQuery
   - Dashboard visualizes key insights from the data

## Future Improvements

- Add real-time data ingestion from property listing APIs
- Implement machine learning models for price prediction
- Expand analysis to include more cities and property types
- Add user authentication for the dashboard
- Implement data quality monitoring
- Add alerting for pipeline failures

## Troubleshooting

### Common Issues

1. **Kaggle API Authentication**:
   - Ensure your Kaggle API key is correctly set up
   - Check that the `~/.kaggle/kaggle.json` file has the correct permissions

2. **Docker Compose Issues**:
   - Ensure Docker and Docker Compose are installed
   - Check that ports 8080 and 8181 are not already in use

3. **GCP Authentication**:
   - Verify that the service account key is correctly placed
   - Ensure the service account has the necessary permissions

### Getting Help

If you encounter any issues, please:
1. Check the logs using `docker-compose logs [service_name]`
2. Refer to the documentation for the specific tool
3. Open an issue in the GitHub repository

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

To contribute:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- Data sources from Kaggle
- Inspiration from real estate market analysis
- Thanks to all the open-source tools that made this project possible

