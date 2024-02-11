FROM python:3.6-slim-buster

WORKDIR /app

COPY requirment.txt ./

RUN pip install -r requirment.txt

COPY . .

EXPOSE 4000

CMD [ "flask","run","--host=0.0.0.0","--port=4000" ]