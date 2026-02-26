FROM python:3.13

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src .
EXPOSE 8000

ENTRYPOINT ["fastapi", "run", "main.py"]