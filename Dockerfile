FROM python:alpine3.10
WORKDIR /app
RUN apk add gcc musl-dev
ADD requirements.txt /app
RUN pip install -r requirements.txt
ADD . /app
CMD ["python", "main.py"]