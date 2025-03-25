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