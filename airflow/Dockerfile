FROM apache/airflow:2.10.3
COPY requirements.txt .
USER root
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 -y
USER 1001
RUN pip install -r requirements.txt