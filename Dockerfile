FROM gcr.io/google_appengine/python
RUN virtualenv /env

# source venv/bin/activate
ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH

# redis and mongo port
EXPOSE 6379 27017

ADD requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

ADD . /app

CMD gunicorn -w 2 -b :$PORT app:app
