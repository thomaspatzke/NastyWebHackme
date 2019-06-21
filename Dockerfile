FROM python:3.6
RUN pip install flask
COPY . /webapp
EXPOSE 8001
WORKDIR /webapp
ENTRYPOINT python BrokenApp.py 0.0.0.0
