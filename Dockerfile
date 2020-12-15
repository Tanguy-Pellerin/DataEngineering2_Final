FROM python:3.6

WORKDIR /app

ENV FLASK_APP=search_app.py

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000
EXPOSE 8050

CMD ["python","search_app.py"]