# Step 1: Use a lightweight, clean official Python environment
FROM python:3.10-slim

# Step 2: Enforce internal container system working path boundary
WORKDIR /app

# Step 3: Install core system compilation modules required for package locks
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Step 4: Inject and cache dependencies pipelines independently
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Mirror the remaining backend service code arrays
COPY . .

# Step 6: Expose the verified internal network socket port
EXPOSE 8000

# Step 7: Launch the production ASGI web server via Uvicorn flags variables
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
