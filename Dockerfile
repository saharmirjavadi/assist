
FROM python:3.9.12-slim

# Install libpq-dev for psycopg2 and development tools
RUN apt update && apt install -y libpq-dev build-essential git

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]