
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
# run this command to install all dependencies
RUN pip install -r requirements.txt

# start server
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "NextDoor.NextDoor.wsgi"]

# run manage.py on port 8000
RUN python manage.py runserver
