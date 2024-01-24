FROM python:3.11-slim-buster

# INSTALL
RUN apt-get -y update
RUN apt-get -y install git

# CLEANUP
RUN apt-get clean

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Run app.py when the container launches
CMD ["python", "/app/webhook_server.py"]