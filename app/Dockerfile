FROM python:3.11-slim
ENV DockerHOME=/usr/src/app

WORKDIR $DockerHOME  

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
 
RUN pip install --upgrade pip  

COPY . .
COPY requirements.txt .
RUN pip install -r requirements.txt 

# RUN ./env/bin/python manage.py initgroups
# RUN ./env/bin/python manage.py crontab add

CMD python manage.py runserver 0.0.0.0:8000