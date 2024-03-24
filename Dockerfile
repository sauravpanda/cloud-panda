# Use the official Python 3.9 image as the base
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Flask app code to the working directory
COPY . .

# Expose the port on which the Flask app will run
EXPOSE 5000

# Set the command to run the Flask app
CMD ["python", "app.py"]

# in Prod
# CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app