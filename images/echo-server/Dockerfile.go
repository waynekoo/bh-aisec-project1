# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app/install/
# Assuming requirements.txt is located at install/requirements.txt in your host machine
COPY install/requirements.txt /app/install/requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r /app/install/requirements.txt

# Copy the entire application code into the container at /app
# Assuming your Flask app file is named app.py and is in the root of your project
COPY . /app

# Expose the port that the Flask app will run on
EXPOSE 5000

# Define environment variable for Flask
ENV FLASK_APP=app.py

# Run the Flask application when the container starts
# Using '0.0.0.0' as host to make it accessible from outside the container
CMD ["flask", "run", "--host=0.0.0.0", "--port=8081"]
