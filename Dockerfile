FROM python:3.9-slim

# Create a non-root user and switch to that user
RUN adduser --disabled-password --gecos '' appuser

# Set the working directory and switch to the non-root user
WORKDIR /app
USER appuser

# Update pip and setuptools
RUN pip install --upgrade pip setuptools

# Copy requirements.txt first to leverage Docker cache
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /app

EXPOSE 5555

# Step 6: Define the command to run your app using Uvicorn
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "5555"]
