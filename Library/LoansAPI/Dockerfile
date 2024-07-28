# Use an official Python runtime as the base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /LoansAPI

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application files to the working directory
COPY . .

EXPOSE 5002

# Run the Flask application
CMD ["python", "main.py"]
