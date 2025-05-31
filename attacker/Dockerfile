FROM python:3.9-slim
WORKDIR /app
COPY sqli_attack.py .
COPY xss_attack.py .
RUN pip install requests
CMD ["sh", "-c", "python sqli_attack.py && python xss_attack.py"]
