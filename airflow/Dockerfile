FROM apache/airflow:2.10.3
COPY requirements.txt .
USER root
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsm6 \
    libxext6 \
    curl \
    && mkdir -p /usr/local/lib/docker/cli-plugins \
    && curl -SL https://github.com/docker/buildx/releases/download/v0.19.2/buildx-v0.19.2.linux-amd64 \
    -o /usr/local/lib/docker/cli-plugins/docker-buildx \
    && chmod +x /usr/local/lib/docker/cli-plugins/docker-buildx
USER 1000
RUN pip install -r requirements.txt