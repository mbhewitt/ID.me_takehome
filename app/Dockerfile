FROM python:3.10-slim-bullseye

WORKDIR /app

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY alphaadvantage.py .

CMD ["python3", "alphaadvantage.py"]
