
FROM python:3.10.4
WORKDIR /NextDoor
RUN python3 -m pip install --upgrade pip
COPY .. .
RUN python3 -m pip install -r requirements.txt
RUN pip install gunicorn
CMD gunicorn NextDoor.wsgi