FROM python:3.9
WORKDIR /app
ADD . /app
RUN python3 -m pip install bottle
EXPOSE 8080
CMD ["python3","server.py"]
