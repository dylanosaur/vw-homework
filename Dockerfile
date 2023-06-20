# Use the official Python base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file to the working directory
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code to the working directory
COPY . .

# Set environment variables
ENV POSTGRES_USER=myuser
ENV POSTGRES_PASSWORD=mypassword
ENV POSTGRES_HOST=db
ENV POSTGRES_PORT=5432
ENV POSTGRES_DB=mydatabase

# Install PostgreSQL client
RUN apt-get update && apt-get install -y postgresql-client

# Expose the Flask app port
EXPOSE 5000

# Run the PostgreSQL service and Flask app
CMD service postgresql start && python app.py
