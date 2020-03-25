FROM tiangolo/uvicorn-gunicorn-fastapi:python3.6

ADD ./app/requirements.txt /app/requirements.txt
WORKDIR /app
RUN python -m pip install -r requirements.txt
COPY ./app /app