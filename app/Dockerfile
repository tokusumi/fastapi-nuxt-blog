FROM tiangolo/uvicorn-gunicorn-fastapi:python3.6

ADD requirements.txt /app/requirements.txt
WORKDIR /app
RUN python -m pip install -r requirements.txt
COPY . /app