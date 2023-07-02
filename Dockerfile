# Select the base image
FROM python:3.10

# Set the working directory
WORKDIR /emsapp

# Copy the application code into the Docker image
COPY . /emsapp

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port on which your backend application is running
EXPOSE 8000

# Specify the command to start your backend server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
