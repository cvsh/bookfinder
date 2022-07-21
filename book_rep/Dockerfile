FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /source
COPY requirements.txt /source
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY manage.py /source
COPY . /source