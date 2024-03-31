FROM python:3.10-slim-buster
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "app.appb:app", "--host", "0.0.0.0", "--port", "7500"]