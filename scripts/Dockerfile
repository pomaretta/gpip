FROM python:3.8

WORKDIR /app

COPY . .

RUN python3 /app/scripts/ci/installer

CMD [ "/app/scripts/optimize.py" ]