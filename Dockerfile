FROM python:3.10

WORKDIR /app_task

COPY . /app_task

COPY gcp_credentials.json /app_task/gcp_credentials.json

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

ENV DOTENV_PATH=/app/.env

CMD ["gunicorn", "-b", "0.0.0.0:8080", "-w", "2", "--threads", "2", "wsgi:app"]
