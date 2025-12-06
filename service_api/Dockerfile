FROM python:3.13.7-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 2001

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYHTONUNBUFFERED 1

CMD ["python", "main.py"]
