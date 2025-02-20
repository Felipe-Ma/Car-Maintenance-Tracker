# Use the official Python Image
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy the proect files
COPY . .

# Install the dependencies
RUN pip install -r requirements.txt

# Expose the port the app runs on
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]