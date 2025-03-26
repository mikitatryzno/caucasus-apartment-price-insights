FROM fishtownanalytics/dbt:1.0.0

# Install additional dependencies
RUN pip install --no-cache-dir \
    dbt-bigquery==1.0.0 \
    pandas==1.5.3

# Set working directory
WORKDIR /dbt

# Command to run when container starts
CMD ["bash"]