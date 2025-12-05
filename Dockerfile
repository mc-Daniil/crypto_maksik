FROM python:3.11-slim@sha256:193fdd0bbcb3d2ae612bd6cc3548d2f7c78d65b549fcaa8af75624c47474444d

WORKDIR /app

RUN adduser appuser

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src .

USER appuser

CMD ["python", "bot.py"]
