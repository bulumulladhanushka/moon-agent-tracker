FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Let k8s override if needed, but by default runs app.py
CMD ["python", "app.py"]
