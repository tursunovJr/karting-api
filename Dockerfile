FROM python:3.9.6-slim
LABEL maintainer="Alexander Zotkin <alexander.zotkin@qoollo.com>"
RUN pip install --upgrade pip
WORKDIR /api
COPY requirements.txt .
RUN pip install -r requirements.txt
ENV FLASK_ENV=production
COPY . .
EXPOSE 8080
ENTRYPOINT ["python", "./start.py"]