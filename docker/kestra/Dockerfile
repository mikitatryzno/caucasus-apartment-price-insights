FROM kestra/kestra:latest

# Install additional dependencies
USER root
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /tmp/
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt

# Create directory for flows
RUN mkdir -p /app/flows /app/storage

# Switch back to kestra user
USER kestra

# Expose port
EXPOSE 8080