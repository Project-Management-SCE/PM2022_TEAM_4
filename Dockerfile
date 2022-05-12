FROM python:3.10.4-alpine
WORKDIR /NextDoor
ADD . /NextDoor
RUN python3 -m pip install --upgrade pip
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
RUN python manage.py makemigrations
RUN python manage.py migrate
RUN python manage.py RUNSERVER
CMD ["python", "NextDoor.py"]