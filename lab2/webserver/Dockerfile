FROM ubuntu
RUN apt-get update
RUN apt-get -y install python3
EXPOSE 8000
ENTRYPOINT ["python3", "-m", "http.server", "8000"]
