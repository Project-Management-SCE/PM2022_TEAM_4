
FROM python:3.10.4
WORKDIR /NextDoor
COPY * /
RUN python3 -m pip install --upgrade pip
COPY requirements.txt ./requirements.txt
RUN python3 -m pip install -r requirements.txt
CMD ["python manage.py runserver"]