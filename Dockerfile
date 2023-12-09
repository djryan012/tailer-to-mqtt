FROM docker:latest

WORKDIR /app

RUN apk --update add python3 py3-pip

COPY log_reader.py .

CMD ["python3", "log_reader.py"]
