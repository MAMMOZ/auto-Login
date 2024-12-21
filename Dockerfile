FROM python:3.9-slim

WORKDIR /app

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
