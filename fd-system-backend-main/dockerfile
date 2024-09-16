FROM python:3.10.12

ARG DB_PASSWORD_GH
ARG SECRET_KEY_GH

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV APP_ENV=stage

ENV DB_PASSWORD=$DB_PASSWORD_GH
ENV SECRET_KEY=$SECRET_KEY_GH

RUN apt-get update \
    && apt-get install -y libpq-dev git make automake gcc g++ subversion openssh-client

WORKDIR /app

COPY requriements.txt /app/
RUN pip install -r requriements.txt

COPY . /app/

EXPOSE 8000

CMD ["python", "manage.py", "runserver"]
