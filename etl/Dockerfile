FROM python:3.9.1
RUN pip install --no-cache-dir pandas sqlalchemy psycopg2
WORKDIR /app
COPY etl_script.py .
CMD ["python", "etl_script.py"]