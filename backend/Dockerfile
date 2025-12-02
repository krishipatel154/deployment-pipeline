# 1. Choose a Python Base Image
FROM python:3.11-slim

# 2. Set the working directory
WORKDIR /app

# 3. Copy requirements and install dependencies
# Note: requirements.txt is the file you use instead of package.json
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy the rest of your application code
COPY . .

# 5. Expose the port your Python app runs on (e.g., Flask/Django default)
# EXPOSE 8000

# This CMD runs Uvicorn for production:
# 1. 'main:app': Your application entry point (module:application_instance)
# 2. '--host 0.0.0.0': ESSENTIAL for external access to the container
# 3. '--port 5000': Matches the EXPOSE port
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]