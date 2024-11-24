FROM python:3.9-slim 
# Maybe don't use slim? Testing req'd

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# EXPOSE 5000

ENV FLASK_APP=app.py

CMD ["flask", "run", "app.py"]