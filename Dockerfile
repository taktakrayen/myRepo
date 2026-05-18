# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requiremments.txt .
RUN pip install --no-cache-dir -r requiremments.txt

COPY . .

EXPOSE 3000

CMD ["python", "manage.py", "runserver", "0.0.0.0:3000"]
