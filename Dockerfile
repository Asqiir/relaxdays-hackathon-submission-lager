FROM python:3.9
WORKDIR /app
ADD . /app
RUN python3 -m pip install bottle
RUN python3 -m pip install pyyaml
EXPOSE 8080
CMD ["python3","server.py"]
