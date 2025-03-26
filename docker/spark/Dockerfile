FROM bitnami/spark:3.3

USER root

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