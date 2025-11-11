# ---------- Base Image ----------
FROM python:3.11-slim

# ---------- System Dependencies ----------
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
    libasound2 \
    libatk1.0-0 \
    libcups2 \
    libxkbcommon0 \
    libxdamage1 \
    libpangocairo-1.0-0 \
    libcairo2 \
    libatspi2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# ---------- Work Directory ----------
WORKDIR /app

# ---------- Copy Requirements ----------
COPY requirements.txt .

# ---------- Install Dependencies ----------
RUN pip install --no-cache-dir -r requirements.txt
RUN playwright install-deps
RUN playwright install chromium

# ---------- Environment Variables ----------
ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright
ENV PORT=10000

# ---------- Copy Application ----------
COPY . .

# ---------- Run Flask ----------
CMD ["python", "app.py"]
