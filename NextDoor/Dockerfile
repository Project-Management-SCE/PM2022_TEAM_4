FROM python:3.10.4-alpine

RUN python3 -m pip install --upgrade pip
COPY . /NextDoor
WORKDIR /NextDoor

RUN python3 -m pip install -r requirements.txt

CMD ["python","tests.py"]