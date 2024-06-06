FROM python:3.10-slim-bookworm
WORKDIR /app
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY src src
ENTRYPOINT ["python","src/main.py"]Ò
