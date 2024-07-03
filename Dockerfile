FROM python:3.9-slim

WORKDIR /app

# Install required libraries using pip
RUN pip install mysql-connector-python pandas

# Copy your Python application code (optional)
COPY . .

# Specify the command to run when the container starts
CMD ["python", "your_app.py"]  # Replace with your application's entry point
