FROM python:3.9-slim

WORKDIR /app

# Install virtualenv
RUN pip install --upgrade pip setuptools virtualenv

# Create a virtual environment
RUN python -m venv /venv

# Activate the virtual environment and install dependencies
RUN /venv/bin/pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /app

EXPOSE 8000

# Step 6: Define the command to run your app using Uvicorn inside the virtual environment
CMD ["/venv/bin/uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
