FROM python:3.10.5
WORKDIR /app
COPY ./requirements.txt /app/requirements.txt 
COPY .env /app/.env
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]

