FROM python:3.11.0

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip3 install --upgrade pip
COPY ./requirements.txt .
RUN pip3 install -r requirements.txt

RUN apt-get -y update && apt-get -y install postgresql postgresql-client gcc python3-dev musl-dev netcat lsof procps

COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

COPY . .

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]