# bazowy obraz
FROM python:3.10-slim

# update
RUN apt-get update && \
    apt-get install -y sudo

# kopiowanie plikow
WORKDIR /application
COPY . /application

## instalacja poetry jako global w kontenerze
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-root

## start aplikacji po calym utworzeniu kontenera
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
