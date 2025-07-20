FROM python:3.12

WORKDIR /app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY ./src ./src
COPY ./keys ./keys

EXPOSE 8000

CMD ["fastapi", "run", "src/main.py", "--port", "8000"]
