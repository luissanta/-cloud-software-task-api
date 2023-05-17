FROM python:3.10

WORKDIR /app_task

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

EXPOSE 5002

CMD ["gunicorn", "-b", "0.0.0.0:5002", "-w", "2", "--threads", "2", "wsgi:app"]