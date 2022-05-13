
# base image
FROM python:3.10.4
# setup environment variable

# port where the Django app runs
EXPOSE 8000
# set work directory


# where your code lives
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip

# copy whole project to your docker home directory.
COPY . /app/
COPY . /PM2022_TEAM-4/
# run this command to install all dependencies
RUN pip install -r requirements.txt

# start server
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser


CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
