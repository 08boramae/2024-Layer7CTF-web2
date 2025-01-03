FROM python:3.11-slim

WORKDIR /app
COPY . /app/
RUN pip install -r requirements.txt
RUN apt-get update
RUN apt-get install -y wget
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt-get install -y ./google-chrome-stable_current_amd64.deb
EXPOSE 8000

CMD ["uvicorn", "main:app", "--port=8000", "--host=0.0.0.0"]