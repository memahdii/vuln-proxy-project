FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip install flask requests
EXPOSE 8000
CMD ["python", "proxy.py"]
