
# base image
FROM python:3.10.4
# setup environment variable
EXPOSE 8000
ENV DockerHOME=/app

# set work directory
RUN mkdir -p $DockerHOME

# where your code lives
WORKDIR $DockerHOME

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip

# copy whole project to your docker home directory.
COPY . $DockerHOME
# run this command to install all dependencies
RUN pip install -r requirements.txt
# port where the Django app runs

RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# run the Django app
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "NextDoor.wsgi"]




