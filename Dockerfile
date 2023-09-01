FROM python:3.7

ENV PYTHONUNBUFFERED=1
ENV DEBUG=True
WORKDIR /usr/src/app 
COPY requirements.txt .

#RUN pip install virtualenvwrapper
#RUN python3 -m venv /venv
#RUN /venv/bin/pip install -U pip
#RUN /venv/bin/pip install --upgrade  pip
RUN pip install -r requirements.txt