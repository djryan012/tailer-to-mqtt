FROM docker:latest

WORKDIR /app

COPY log_reader.py .

CMD ["python", "log_reader.py"]