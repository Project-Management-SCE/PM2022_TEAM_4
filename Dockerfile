FROM python:3.10.4-alpine
WORKDIR /app
ADD . /app
RUN pip install -r requirements.txt
CMD ["python", "app.py"]