# Use the wngr/garmindb image as the base image
FROM wngr/garmindb

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-dev \
    python3-venv \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create and activate virtual environment
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Upgrade pip
RUN pip install --upgrade pip

# Copy the requirements.txt file into the container
#COPY requirements.txt .

# Install the required Python packages
#RUN pip install --no-cache-dir -r requirements.txt

# Set the working directory
# WORKDIR /app
WORKDIR /root

# Create the data directory
RUN mkdir -p /root/HealthData

# Copy the application code
COPY . .

# Copy the GarminConnectConfig.json file
COPY GarminConnectConfig.json /root/.GarminDb/GarminConnectConfig.json

# Set the command to start the application
CMD ["python3", "/root/.GarminDb/GarminDbLauncher.py"]


# Create the app.py file
# RUN echo "print('Hello from the garmindb app!')" > app.py


# Run the application (sample)
# CMD ["python3", "app.py"]