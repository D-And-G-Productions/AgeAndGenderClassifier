FROM python:3.11-slim
WORKDIR /app

# Copy requirements and install them
COPY webapp/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your application code
COPY webapp/ .

EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]