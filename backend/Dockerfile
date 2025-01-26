# Use a Python base image
FROM python:3.10-slim

# Create a working directory
WORKDIR /code

# Copy requirements first (to utilize Docker's caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . .

# Expose the port (not strictly necessary, but good practice)
EXPOSE 8000

# Run the FastAPI app with Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"] 