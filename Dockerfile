#aici creeam IMAGINEA containerului
#(de fiecare data cand modificam ceva o RECONSTRUIESTE)

FROM python:3.11-slim
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
#instalează toate librăriile Python din requirements.txt

COPY app/ app/ 
#din folderul local app/→ în container,în app/
COPY keys/ keys/ 

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
#comanda care pornește containerul

# uvicorn = server
# app.main:app = fișier app/main.py, variabila app
# 0.0.0.0 = acceptă conexiuni din afara containerului
# 8000 = portul aplicației


