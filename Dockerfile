FROM gboeing/osmnx:latest
WORKDIR /home/jovyan/work
ADD requirements.txt /home/jovyan/work
RUN pip install -r requirements.txt
ADD *.py /home/jovyan/work/
CMD ["gunicorn", "flask_app:app", "-b", "0.0.0.0:5000", "-t", "90"]
