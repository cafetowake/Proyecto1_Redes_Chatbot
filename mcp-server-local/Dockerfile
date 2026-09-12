FROM python:3.11-slim

WORKDIR /app

COPY catalog.py protocol.py server_http.py ./

EXPOSE 8081

CMD ["python3", "server_http.py"]