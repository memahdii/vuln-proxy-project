FROM python:3.9-slim
WORKDIR /app
COPY sqli_attack.py .
RUN pip install requests
CMD ["python", "sqli_attack.py"]
