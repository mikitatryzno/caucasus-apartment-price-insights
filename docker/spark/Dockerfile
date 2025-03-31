FROM bitnami/spark:3.3

USER root

# Install wget and other necessary packages
RUN apt-get update && apt-get install -y wget && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Install GCP connector for Spark
RUN wget -P /opt/bitnami/spark/jars/ https://storage.googleapis.com/hadoop-lib/gcs/gcs-connector-hadoop3-latest.jar

# Create directories for jobs and data
RUN mkdir -p /opt/spark/jobs /opt/spark/data

# Set permissions
RUN chmod -R 777 /opt/spark/jobs /opt/spark/data

# Switch back to non-root user
USER 1001