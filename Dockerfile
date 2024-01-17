# Use the official Python base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install the Python dependencies
RUN pip install -r requirements.txt

RUN mkdir -p /home/ivan/Projects/Charisma/google-trends/files/

RUN apt-get update && apt-get install -y wget unzip && \ 
    wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt install -y ./google-chrome-stable_current_amd64.deb && \
    rm google-chrome-stable_current_amd64.deb && \
    apt-get clean

# Copy the application code to the working directory
COPY . .

# Expose the port on which the application will run
EXPOSE 8000

RUN alembic upgrade head --sql

RUN alembic upgrade head

# Run the FastAPI application using uvicorn server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]