FROM python:3.11-slim

WORKDIR /code

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]


# Ideea simplă:

# FROM = ia Python gata instalat
# WORKDIR = folderul din container
# COPY requirements.txt = copiază dependențele
# RUN pip install = le instalează
# COPY ./app ./app = copiază backendul
# CMD = pornește FastAPI