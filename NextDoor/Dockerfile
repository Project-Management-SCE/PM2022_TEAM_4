
FROM jenkins:1.596

USER root
RUN apt-get update \
      && apt-get install -y sudo \
      && rm -rf /var/lib/apt/lists/*
RUN echo "jenkins ALL=NOPASSWD: ALL" >> /etc/sudoers

USER jenkins
COPY plugins.txt /usr/share/jenkins/plugins.txt
RUN /usr/local/bin/plugins.sh /usr/share/jenkins/plugins.txt

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