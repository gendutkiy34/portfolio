FROM alpine:latest

WORKDIR /app
COPY requirements.txt requirements.txt
RUN mkdir /app/logs
RUN apk add python3
RUN apk add py-pip
RUN pip install -r requirements.txt
RUN pip install python-telegram-bot -U --pre
RUN pip freeze
COPY * /app/
CMD ["python3","/app/main.py"]
