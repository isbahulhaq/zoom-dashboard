FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    wget \
    libnss3 \
    libx11-6 \
    libxcomposite1 \
    libxcursor1 \
    libxi6 \
    libxtst6 \
    libglib2.0-0 \
    libgl1 \
    libfontconfig1 \
    libxrandr2 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN playwright install chromium

COPY . .

CMD ["python", "app.py"]
