ARG PYTHON_VERSION=3.10.7
FROM python:${PYTHON_VERSION}

ADD main.py /
ADD requirements.txt /

RUN pip install -r requirements.txt

CMD python -m main
