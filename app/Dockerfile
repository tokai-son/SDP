FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir tornado
RUN pip install --no-cache-dir aioredis

# Make port 9999 available to the world outside this container
EXPOSE 9999

# Run app.py when the container launches
CMD ["python", "main.py"]
