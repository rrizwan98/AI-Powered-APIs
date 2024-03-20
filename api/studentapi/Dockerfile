# Use the official Python 3.10 slim image as the base image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY . /app
COPY .env /app/.env

# Install the Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# # Copy the rest of the application code into the container

# # Set the command to run the application
CMD uvicorn main:app --reload --port=8000 --host=0.0.0.0




# env/
# __pycache__

# *.env
# *.env.*
# .env*