ARG PYTHON_VERSION=3.10.7
FROM python:${PYTHON_VERSION}

WORKDIR /app
ADD . /app

RUN pip install -r requirements.txt

CMD python -m main
