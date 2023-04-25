FROM python:3.10

WORKDIR /app_task

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

CMD ["celery", "-A", "app.celery.tasks_celery", "worker", "-l", "info", "--pool=solo", "-Q", "response"]
