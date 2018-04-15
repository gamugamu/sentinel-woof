FROM gcr.io/google_appengine/python
RUN virtualenv /env

# source venv/bin/activate
ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH

# redis, mongo and postgreport
EXPOSE 6379 27017 5432

# Install prerequisites
ADD requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

ADD . /app

CMD gunicorn -w 4 -b :$PORT app:app
